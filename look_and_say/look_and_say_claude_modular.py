import sys
import time
from pathlib import Path

def initialize_sequence():
    starting_sequence = '1223334444'
    return starting_sequence

def apply_look_and_say(current_sequence):
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
    return current_sequence

def iterate_look_and_say(starting_sequence, n):
    i = 0
    while i < n:
        if i == 0:
            current_sequence = starting_sequence
        else:
            current_sequence = apply_look_and_say(current_sequence)
        i += 1
    seq = current_sequence
    return seq

def main(N):
    starting_sequence = initialize_sequence()
    n = N
    seq = iterate_look_and_say(starting_sequence, n)
    return seq

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:')
        print('     python ' + sys.argv[0] + ' N')
        print('Please specify a number.')
        sys.exit()

    N = int(sys.argv[1])
    t0 = time.perf_counter()
    main(N)
    print(time.perf_counter() - t0)
