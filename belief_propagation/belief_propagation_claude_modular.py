import numpy as np
import sys
import time
from pathlib import Path

def generate_matrix(dim):
    np.random.seed(0)
    A = np.random.rand(dim, dim)
    return A

def initialize_beliefs(dim):
    x = np.ones((dim,))
    return x

def propagate_message(A, x):
    x = np.log(np.dot(A, np.exp(x)))
    return x

def normalize_beliefs(x):
    x = x - np.log(np.sum(np.exp(x)))
    return x

def run_belief_propagation(A, x, N):
    for i in range(N):
        x = propagate_message(A, x)
        x = normalize_beliefs(x)
    return x

def main(N):
    dim = 5000
    A = generate_matrix(dim)
    x = initialize_beliefs(dim)
    x = run_belief_propagation(A, x, N)
    y = x
    return y

if __name__ == '__main__':
    N = int(sys.argv[1])
    dti = time.perf_counter()
    main(N)
    print(time.perf_counter() - dti)
