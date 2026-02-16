import numpy as np
import numpy.random as rn
import sys
import time

n = int(sys.argv[1])
dt1 = time.perf_counter()

for i in range(100, n + 1, 100):
    """
        Compute the FFT of an n-by-n matrix of data
    """
    print(f'Executando FFT para n={i}')
    rn.seed(0)
    matrix = rn.rand(i, i) + 1j * rn.randn(i, i)
    result = np.fft.fft2(matrix)
    result = np.abs(result)

print(time.perf_counter() - dt1)