import sys
import numpy as np
from itertools import combinations
from collections import Counter
import datetime as dt
np.random.seed(0)

if __name__ == '__main__':
    N = float(sys.argv[1])

    G = N
    N = 12162
    L = 156
    mu = 3e-08
    repeat_alleles = list()
    for i in range(N):
        num_mutations = np.random.poisson(L * mu * G)
        positions = np.random.choice(range(L), size=num_mutations, replace=False)
        repeat_alleles.append(positions)
    x = repeat_alleles

    t1 = dt.datetime.now()

    sims = x
    counts = Counter()
    i = 0
    for p1, p2 in combinations(sims, 2):
        if i % 10000000 == 0:
            print('\ttotal pairs counted: %d\n' % i)
        i += 1
        temp1 = set(p1)
        num_shared = len(temp1.intersection(set(p2)))
        counts[num_shared] += num_shared
    shared_counts = counts

    t2 = dt.datetime.now()
    temp2 = t2 - t1
    print('took', temp2.seconds, 'seconds to do pairwise comparisons')
    print(shared_counts)
