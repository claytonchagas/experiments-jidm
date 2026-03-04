import numpy as np
import sys
from pathlib import Path
import time

def define_integration_bounds():
    a = -3.0
    b = 3.0
    return a, b

def compute_leggauss(n):
    x, w = np.polynomial.legendre.leggauss(n)
    return x, w

def transform_quadrature_points(x, a, b):
    t = 0.5 * (x + 1) * (b - a) + a
    return t

def evaluate_integrand(t):
    result = np.exp(t)
    return result

def compute_integral(w, integrand_values, a, b):
    result = sum(w * integrand_values) * 0.5 * (b - a)
    return result

def main(order):
    n = order
    a, b = define_integration_bounds()
    x, w = compute_leggauss(n)
    t = transform_quadrature_points(x, a, b)
    integrand_values = evaluate_integrand(t)
    compute_integral(w, integrand_values, a, b)

if __name__ == '__main__':
    order = int(sys.argv[1])
    dti = time.perf_counter()
    main(order)
    print(time.perf_counter() - dti)
