import sys
import numpy as np
from itertools import combinations
from collections import Counter
import datetime as dt

np.random.seed(0)

N = float(sys.argv[1])

"""
    Generate N repeats of length L mutating at rate
    mu for G generations.
"""
repeat_alleles = list()
for i in range(12162):
    num_mutations = np.random.poisson(156 * 3e-08 * N)
    positions = np.random.choice(range(156), size=num_mutations, replace=False)
    repeat_alleles.append(positions)
x = repeat_alleles

t1 = dt.datetime.now()

counts = Counter()
i = 0
for p1, p2 in combinations(x, 2):
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