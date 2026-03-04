import numpy as np
import numpy.random as rn
import sys
import time

def seed_random():
    rn.seed(0)

def generate_complex_matrix(n):
    real_part = rn.rand(n, n)
    imag_part = rn.randn(n, n)
    matrix = real_part + 1j * imag_part
    return matrix

def compute_fft2(matrix):
    result = np.fft.fft2(matrix)
    return result

def compute_magnitude(result):
    result = np.abs(result)
    return result

def compute_FFT(n):
    print(f'Executando FFT para n={n}')
    seed_random()
    matrix = generate_complex_matrix(n)
    result = compute_fft2(matrix)
    result = compute_magnitude(result)
    return result

def main(n):
    for i in range(100, n + 1, 100):
        compute_FFT(i)

if __name__ == '__main__':
    n = int(sys.argv[1])
    dt1 = time.perf_counter()
    main(n)
    print(time.perf_counter() - dt1)
