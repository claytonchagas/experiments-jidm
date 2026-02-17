import time
import sys
import os
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import imageio
import math
from scipy.sparse import csr_matrix

if __name__ == '__main__':
    n = float(sys.argv[1])

    dimensionality = (2, 2)
    nx = 0.15
    ny = 0.15
    delta_t = n
    start_time = time.perf_counter()

    shape = (int(dimensionality[0] / nx), int(dimensionality[1] / ny))

    matrix = np.zeros(shape)
    for x in [0, len(matrix) - 1]:
        for y in range(len(matrix[x])):
            matrix[x][y] = 2 * (x * nx) + (y * ny) ** 2
    for y in [0, len(matrix[0]) - 1]:
        for x in range(len(matrix)):
            matrix[x][y] = 2 * (x * nx) + (y * ny) ** 2
    current_distribution = matrix

    directory = 'images/tmp/'
    if os.path.exists(directory):
        files = os.listdir(directory)
        for filename in files:
            os.remove(os.path.join(directory, filename))

    ax = sns.heatmap(current_distribution, cmap='coolwarm')
    if not os.path.exists('images/tmp'):
        os.makedirs('images/tmp')
    plt.savefig('images/tmp/img_' + str(time.time()) + '.png')
    plt.close()

    system_dimension = shape[0] * shape[1]
    system_to_solve = []
    for i in range(system_dimension):
        current_row = [0] * system_dimension
        x_size = shape[0]
        y_size = shape[1]
        if i // x_size == 0:
            current_row[i] = 1
        elif i % x_size == 0:
            current_row[i] = 1
        elif (i + 1) % x_size == 0:
            current_row[i] = 1
        elif i // x_size == y_size - 1:
            current_row[i] = 1
        else:
            current_row[i] = 2 * delta_t * (nx ** 2 + ny ** 2) / (nx ** 2 * ny ** 2) + 1.0
            current_row[i - shape[0]] = -delta_t / nx ** 2
            current_row[i + shape[0]] = -delta_t / nx ** 2
            current_row[i - 1] = -delta_t / ny ** 2
            current_row[i + 1] = -delta_t / ny ** 2
        sparse_row = csr_matrix(current_row)
        system_to_solve.append(sparse_row)

    max_difference = 1.0
    while max_difference > 0 and math.log(max_difference, 10) > -7:
        linearized_distribution = current_distribution.reshape(shape[0] * shape[1])

        A = system_to_solve
        B = linearized_distribution

        nA = len(A)
        L = [[0.0] * nA for i in range(nA)]
        U = [[0.0] * nA for i in range(nA)]
        for j in range(nA):
            L[j][j] = 1.0
            for i in range(j + 1):
                soma = 0
                for k in range(i):
                    soma += U[k][j] * L[i][k]
                a = A[i]
                dense_a_i = np.array(a.todense())
                U[i][j] = dense_a_i[0][j] - soma
            for i in range(j, nA):
                soma = 0
                for k in range(j):
                    soma += U[k][j] * L[i][k]
                a = A[i]
                dense_a_i = np.array(a.todense())
                L[i][j] = (dense_a_i[0][j] - soma) / U[j][j]

        nR = len(A)
        Y_lista = [0 for i in range(nR)]
        X_lista = [0 for i in range(nR)]
        Y_lista[0] = B[0]
        for l in range(1, nR):
            Y_lista[l] = (B[l] - sum((L[l][c] * Y_lista[c] for c in range(nR)))) / L[l][l]
        X_lista[nR - 1] = Y_lista[nR - 1] / U[nR - 1][nR - 1]
        for l in reversed(range(0, nR - 1)):
            X_lista[l] = (Y_lista[l] - sum((U[l][c] * X_lista[c] for c in reversed(range(nR))))) / U[l][l]

        result = np.array(X_lista)

        max_difference = np.max(np.abs(linearized_distribution - result))
        current_distribution = result.reshape(shape[0], shape[1])

        ax = sns.heatmap(current_distribution, cmap='coolwarm')
        if not os.path.exists('images/tmp'):
            os.makedirs('images/tmp')
        plt.savefig('images/tmp/img_' + str(time.time()) + '.png')
        plt.close()

    directory = 'images/tmp/'
    if not os.path.exists('images/gif'):
        os.makedirs('images/gif')
    with imageio.get_writer('images/gif/movie.gif', mode='I', duration=0.5) as writer:
        for filename in sorted(os.listdir(directory)):
            image = imageio.imread(directory + filename)
            writer.append_data(image)
    writer.close()
    if os.path.exists(directory):
        files = os.listdir(directory)
        for filename in files:
            os.remove(os.path.join(directory, filename))

    end_time = time.perf_counter()
    print(end_time - start_time)
