
from gf256 import gf_element as gfe, poly, debug, set_loglevel, x
import time
import random as ran

BLKSIZE = 255
ERRCHARS = 16
MSGCHARS = BLKSIZE - 2 * ERRCHARS
ALPHA = gfe(3)
ZERO = poly([gfe(0)])

def encode_block(message):
    global MSGCHARS, ERRCHARS, BLKSIZE, ALPHA
    debug(2, "Constructing message polynomial...")
    msg = poly([gfe(ord(i)) for i in message] + [gfe(0)] * (MSGCHARS - len(message)))
    debug(3, msg.coeffs)
    debug(2, "Encoding message...")
    return [msg(ALPHA ** (i)) for i in range(BLKSIZE)]

def encode(message):
    debug(1,"Organizing the message into blocks of 223...")
    blocks = []
    while len(message)>223:
        blocks.append(message[:223])
        message = message[223:]
    blocks.append(message)
    enc_blocks = []
    for i, block in enumerate(blocks):
        debug(1, "Encoding block Nr.", i+1)
        enc_blocks.append(encode_block(block))
        debug(1, "done")
    return enc_blocks

def decode_block(message):
    global BLKSIZE, ERRCHARS, ALPHA, errcache
    debug(1, "Receiving block")
    respoly = lagrange(message, range(BLKSIZE))
    err_indices = []
    if respoly.deg == 222:
        debug(1, "No errors detected.")
        return "".join(["{0:c}".format(i.val) for i in respoly.coeffs]).strip("\00")
    else:
        debug(1, "The message has errors")
        err_indices = [i for i in errloc(respoly)]
    indices = []
    i = 0
    while len(indices) < MSGCHARS:
        if i not in err_indices:
            indices.append(i)
        i += 1
    res = lagrange([message[i] for i in indices], indices)
    ret = "".join(["{0:c}".format(i.val) for i in res.coeffs]).strip("\00")
    return ret

def decode(blocks):
    debug(1, "Decoding the Message.")
    dec_blocks = []
    for i, block in enumerate(blocks):
        debug(1, "Decoding block Nr.", i+1)
        dec_blocks.append(decode_block(block))
    return "".join(dec_blocks)


def lagrange(values, indices):
    global ALPHA, ZERO
    debug(1, "Interpolating the message polynomial...")
    x_vals = [ALPHA**i for i in indices]
    L = ZERO
    for i, x_i in enumerate(x_vals):
        if i%30 == 0:
            debug(1, "{0:.2f}%".format(100*i/len(x_vals)))
        zaehler = x(0)
        nenner = []
        for j, x_j in enumerate(x_vals):
            if j != i:
                zaehler = zaehler.flshift(1) + zaehler.scale(x_j)
                nenner.append((x_i-x_j))
            else:
                continue
        nenner = gfe.prod(nenner)
        l_i = zaehler.scale(values[i]*nenner.inv())
        L+=l_i
    debug(1, "100.00%")
    return L

def kgV(a, b):
    if a.deg < b.deg:
        a, b = b, a
    a0 = a
    d0, d = ZERO, x(0)
    while b.deg >= MSGCHARS+ERRCHARS:
        tmp = a.divmod(b)
        f = tmp[0]
        a, b = b, tmp[1]
        d0, d = d, f*d+d0
    return d

def errloc(res_poly):
    global BLKSIZE, ALPHA
    debug(1, "Locating errors...")
    n = x(BLKSIZE) - x(0)
    Lambda = kgV(n, res_poly)
    debug(2, "deg(Lambda) =",Lambda.deg)
    X = []
    for i in range(BLKSIZE):
        if Lambda(ALPHA**(i)) == 0:
            X.append(i)
    debug(1, "Errors found at bytes: ", [i for i in X])
    return X

def inserrRB(message, x):
    msg = [i for i in message]
    msg_0 = msg.copy()
    errcache = []
    for i in range(x):
        z = ran.randint(0,254)
        while z in errcache:
            z = ran.randint(0,254)
        errcache.append(z)
        msg[z] += gfe(ran.randint(1,254))
    debug(1,"Errors inserted at positions:",*(i for i in errcache))
    debug(2,msg == msg_0)
    return msg

def inserrRS(blocks, x):
    errcache = []
    for i in range(x):
        z = ran.randint(0,254)
        while z in errcache:
            z = ran.randint(0,254)
        errcache.append(z)
    for block in blocks:
        for i in errcache:
            block[i] += gfe(ran.randint(1,254))
    return blocks

set_loglevel(1)
print("Welcome. Please enter your message:")
message = input()
enc_blocks = encode(message)
print("Would you like to insert some errors into the blocks?")
response = input("[y/N]")
if not "y" in response.lower():
    print(decode(enc_blocks))
    exit(0)
print("Would you like to insert random errors at:\n \
    \trandom bytes for every block (rb)?\n\
    \tthe same set of up to 16 random bytes applied to every block (rs)?")
response = input().lower()
if response == "rb":
    errnums = ran.randint(1,16)
    print("Inserting errors at",errnums,"random positions in each block")
    for block in enc_blocks:
        block = inserrRB(block, errnums)
elif response == "rs":
    errnums = ran.randint(1,16)
    print("Inserting errors at the same",errnums,"positions in every block.")
    enc_blocks = inserrRS(enc_blocks, errnums)

print("Errors inserted")
print(decode(enc_blocks))
