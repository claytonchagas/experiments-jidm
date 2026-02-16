import numpy as np
import sys
from pathlib import Path
import time

if __name__ == '__main__':
    order = int(sys.argv[1])
    dti = time.perf_counter()
    n = order
    a = -3.0
    b = 3.0
    x, w = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (x + 1) * (b - a) + a
    sum(w * np.exp(t)) * 0.5 * (b - a)
    print(time.perf_counter() - dti)