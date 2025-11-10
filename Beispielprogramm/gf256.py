loglevel = 0

def set_loglevel(x):
    global loglevel
    loglevel = x

def debug(x, *args, **kwargs):
    global loglevel
    if loglevel>=x:
        print(*args, *kwargs)

class gf_element():
    # Diese Listen wurden übernommen von: https://github.com/brownan/Reed-Solomon/blob/master/ff.py
    # Die Idee, Eigene Klassen für die Galoiskörperelemente bzw. Polynome zu erstellen und die 
    # Standard Operatoren zu überschreiben stammt auch von dort, der genaue Inhalt der 
    # Funktionen wurde allerdings selbst geschrieben.
    m_lut = (1, 3, 5, 15, 17, 51, 85, 255, 26, 46, 114, 150, 161, 248, 19,
            53, 95, 225, 56, 72, 216, 115, 149, 164, 247, 2, 6, 10, 30, 34,
            102, 170, 229, 52, 92, 228, 55, 89, 235, 38, 106, 190, 217, 112,
            144, 171, 230, 49, 83, 245, 4, 12, 20, 60, 68, 204, 79, 209, 104,
            184, 211, 110, 178, 205, 76, 212, 103, 169, 224, 59, 77, 215, 98,
            166, 241, 8, 24, 40, 120, 136, 131, 158, 185, 208, 107, 189, 220,
            127, 129, 152, 179, 206, 73, 219, 118, 154, 181, 196, 87, 249, 16,
            48, 80, 240, 11, 29, 39, 105, 187, 214, 97, 163, 254, 25, 43, 125,
            135, 146, 173, 236, 47, 113, 147, 174, 233, 32, 96, 160, 251, 22,
            58, 78, 210, 109, 183, 194, 93, 231, 50, 86, 250, 21, 63, 65, 195,
            94, 226, 61, 71, 201, 64, 192, 91, 237, 44, 116, 156, 191, 218,
            117, 159, 186, 213, 100, 172, 239, 42, 126, 130, 157, 188, 223,
            122, 142, 137, 128, 155, 182, 193, 88, 232, 35, 101, 175, 234, 37,
            111, 177, 200, 67, 197, 84, 252, 31, 33, 99, 165, 244, 7, 9, 27,
            45, 119, 153, 176, 203, 70, 202, 69, 207, 74, 222, 121, 139, 134,
            145, 168, 227, 62, 66, 198, 81, 243, 14, 18, 54, 90, 238, 41, 123,
            141, 140, 143, 138, 133, 148, 167, 242, 13, 23, 57, 75, 221, 124,
            132, 151, 162, 253, 28, 36, 108, 180, 199, 82, 246, 1)
    index_lut = (None, 0, 25, 1, 50, 2, 26, 198, 75, 199, 27, 104, 51, 238, 223,
            3, 100, 4, 224, 14, 52, 141, 129, 239, 76, 113, 8, 200, 248, 105,
            28, 193, 125, 194, 29, 181, 249, 185, 39, 106, 77, 228, 166, 114,
            154, 201, 9, 120, 101, 47, 138, 5, 33, 15, 225, 36, 18, 240, 130,
            69, 53, 147, 218, 142, 150, 143, 219, 189, 54, 208, 206, 148, 19,
            92, 210, 241, 64, 70, 131, 56, 102, 221, 253, 48, 191, 6, 139, 98,
            179, 37, 226, 152, 34, 136, 145, 16, 126, 110, 72, 195, 163, 182,
            30, 66, 58, 107, 40, 84, 250, 133, 61, 186, 43, 121, 10, 21, 155,
            159, 94, 202, 78, 212, 172, 229, 243, 115, 167, 87, 175, 88, 168,
            80, 244, 234, 214, 116, 79, 174, 233, 213, 231, 230, 173, 232, 44,
            215, 117, 122, 235, 22, 11, 245, 89, 203, 95, 176, 156, 169, 81,
            160, 127, 12, 246, 111, 23, 196, 73, 236, 216, 67, 31, 45, 164,
            118, 123, 183, 204, 187, 62, 90, 251, 96, 177, 134, 59, 82, 161,
            108, 170, 85, 41, 157, 151, 178, 135, 144, 97, 190, 220, 252, 188,
            149, 207, 205, 55, 63, 91, 209, 83, 57, 132, 60, 65, 162, 109, 71,
            20, 42, 158, 93, 86, 242, 211, 171, 68, 17, 146, 217, 35, 32, 46,
            137, 180, 124, 184, 38, 119, 153, 227, 165, 103, 74, 237, 222, 197,
            49, 254, 24, 13, 99, 140, 128, 192, 247, 112, 7)
    def __init__(self, x):
        if x<0:
            x*=-1
        self.val = x%256
        self.char = "{0:c}".format(x)
    
    def __add__(a, b):
        if b == 0:
            return a
        return gf_element(a.val^b.val)

    def __sub__(a,b):
        return a.__add__(b)
    
    def __radd__(a,b):
        return a.__add__(b)
    
    def __mul__(a, b):
        if a == 0 or b == 0:
            return gf_element(0)
        try:
            return gf_element(gf_element.m_lut[(gf_element.index_lut[a.val]+gf_element.index_lut[b.val])%255])
        except IndexError:
            print(a.val)
            exit(1)
    
    def prod(x):
        return gf_element(gf_element.m_lut[sum([gf_element.index_lut[i.val] for i in x]) % 255])
    
    def __pow__(a, x):
        if a == 0:
            return gf_element(0)
        return gf_element(gf_element.m_lut[(gf_element.index_lut[a.val]*x)%255])
    
    def inv(self):
        if self.val == 0:
            return gf_element(0)
        return gf_element(gf_element.m_lut[255-gf_element.index_lut[self.val]])
    
    def __truediv__(a, b):
        if a == 0:
            return gf_element(0)
        if b == 0:
            raise ValueError("Cannot divide by 0")
        return a*b.inv()
    
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            return self.val == other
        return self.val == other.val
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(self.val)
    
    def __hash__(self):
        return hash(self.val)


class poly():
    def __init__(self, coefficients):
        if coefficients == 0:
            self.coeffs = [gf_element(0)]
        else:
            self.coeffs = [i for i in coefficients]
            while self.coeffs[0] == 0 and len(self.coeffs)>1:
                self.coeffs.pop(0)
        self.udeg()

    def __add__(a, b):
        ac = a.coeffs
        bc = b.coeffs
        match a.deg>b.deg:
            case True:
                bc = [gf_element(0)]*(a.deg-b.deg)+bc
            case False:
                ac = [gf_element(0)]*(b.deg-a.deg)+ac
        return poly(x+y for x,y in zip(ac,bc))

    __sub__ = __add__

    def __mul__(a, b):
        if isinstance(b, gf_element):
            return poly(i*b for i in a.coeffs)
        ac = a.coeffs
        bc = b.coeffs
        res = [gf_element(0) for _ in range(a.deg+b.deg+1)]
        for i, ae in enumerate(ac):
            for j, be in enumerate(bc):
                res[i+j] += ae*be
        return poly(res)
    
    def divmod(a, b):
        dividend = a.coeffs.copy()
        divisor = b.coeffs.copy()
        while(divisor[0] == 0):
            divisor.pop(0)
        quot = []
        while len(dividend) >= len(divisor):
            quot.append(dividend[0]/divisor[0])
            for i in range(len(divisor)):
                dividend[i] -= divisor[i]*quot[-1]
            dividend.pop(0)
        return poly(quot), poly(dividend)

    def __truediv__(self, other):
        if isinstance(other, gf_element):
            return poly([i/other for i in self.coeffs])
        return self.divmod(other)[0]

    def __mod__(self, other):
        return self.divmod(other)[1]
    
    def flshift(self, x):
        c = self.coeffs.copy()
        c += [gf_element(0)]*x
        return poly(c)
    
    def udeg(self):
        self.deg = len(self.coeffs)-1
    
    def eval(self, x):
        return sum([a*x**(self.deg-i) if i != self.deg else a for i, a in enumerate(self.coeffs)])
    
    def __call__(self, x):
        return self.eval(x)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.coeffs[0] == other and self.coeffs[-1] == other
        return self.coeffs == other.coeffs

    def __str__(self):
        res = (str(x)+"x^{"+str(self.deg-y)+"}" for y, x in enumerate(self.coeffs))
        return "+".join(res)
    
    def __repr__(self):
        return str(self.coeffs)
    
    def scale(self, x):
        self.coeffs = [i*x for i in self.coeffs]
        return self


def x(x):
    return poly([gf_element(1)]+[gf_element(0)]*x)