import time
import sys
import numpy as np
import random

def sort_rewards_descending(rewards):
    temp1 = list(rewards)
    a = sorted(temp1.copy(), reverse=True)
    for i in range(len(a)):
        a[i] = int(a[i])
    a = np.array(a)
    return a

def compute_cumulative_probabilities(a):
    p = 1.0 * (np.arange(len(a)) + 1) / len(a)
    return p

def find_quantile_value(a, p, alpha):
    q_a = a[np.where(p >= 1 - alpha)[0][0]]
    return q_a

def extract_tail_subset(a, q_a):
    check = a < q_a
    if np.where(check == True)[0].size == 0:
        ind = 0
        temp = a[:ind + 1]
    else:
        ind = np.where(check == True)[0][0] - 1
        temp = a[:ind + 1]
    return temp

def compute_cvar(temp):
    cvar_result = sum(temp) / len(temp)
    return cvar_result

def main(rewards, alpha):
    a = sort_rewards_descending(rewards)
    p = compute_cumulative_probabilities(a)
    q_a = find_quantile_value(a, p, alpha)
    temp = extract_tail_subset(a, q_a)
    cvar_result = compute_cvar(temp)
    return cvar_result

if __name__ == '__main__':
    random.seed(0)
    n = [random.randint(0, 1000000000) for i in range(int(float(sys.argv[1])))]
    start = time.perf_counter()

    cvar_result = main(n, 0.9)
    print(cvar_result)

    print(time.perf_counter() - start)
