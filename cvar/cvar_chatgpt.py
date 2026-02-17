import time
import sys
import numpy as np

if __name__ == '__main__':
    import random
    random.seed(0)
    n = [random.randint(0, 1000000000) for i in range(int(float(sys.argv[1])))]
    start = time.perf_counter()

    rewards = n
    alpha = 0.9
    temp1 = list(rewards)
    a = sorted(temp1.copy(), reverse=True)
    for i in range(len(a)):
        a[i] = int(a[i])
    a = np.array(a)
    p = 1.0 * (np.arange(len(a)) + 1) / len(a)
    q_a = a[np.where(p >= 1 - alpha)[0][0]]
    check = a < q_a
    if np.where(check == True)[0].size == 0:
        ind = 0
        temp = a[:ind + 1]
    else:
        ind = np.where(check == True)[0][0] - 1
        temp = a[:ind + 1]
    _result = sum(temp) / len(temp)
    print(_result)

    print(time.perf_counter() - start)
