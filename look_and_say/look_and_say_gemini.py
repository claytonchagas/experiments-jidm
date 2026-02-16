import sys
import time
from pathlib import Path

if len(sys.argv) < 2:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' N')
    print('Please specify a number.')
    sys.exit()

N = int(sys.argv[1])
t0 = time.perf_counter()

starting_sequence = '1223334444'
n = N
i = 0
while i < n:
    if i == 0:
        current_sequence = starting_sequence
    else:
        count = 1
        temp_sequence = ''
        for j in range(1, len(current_sequence)):
            if current_sequence[j] == current_sequence[j - 1]:
                count += 1
            else:
                temp_sequence = temp_sequence + str(count) + current_sequence[j - 1]
                count = 1
        temp_sequence = temp_sequence + str(count) + current_sequence[len(current_sequence) - 1]
        current_sequence = temp_sequence
    i += 1
seq = current_sequence

print(time.perf_counter() - t0)