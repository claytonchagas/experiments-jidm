import numpy as np
import sys
from pathlib import Path
import time

order = int(sys.argv[1])
dti = time.perf_counter()

"""
  Perform the Gauss-Legendre Quadrature at the prescribed order n
"""
a = -3.0
b = 3.0
x, w = np.polynomial.legendre.leggauss(order)
t = 0.5 * (x + 1) * (b - a) + a
sum(w * np.exp(t)) * 0.5 * (b - a)

print(time.perf_counter() - dti)