from sympy import Poly
from sympy.abc import x
g = Poly(x**8+x**4+x**3+x+1, modulus=2)
print(g.is_irreducible)
