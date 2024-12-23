#!/usr/bin/env python3
import argparse
from aoc_util import dbg
from collections import defaultdict

def problem(input_file, part2=False):
    left = []
    right = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            l,r = line.split()
            left.append(int(l))
            right.append(int(r))

    if not part2:
        left = sorted(left)
        right = sorted(right)
        return sum(abs(l-r) for l,r in zip(left,right))

    total = 0
    counts = defaultdict(lambda: 0)
    for number in right:
        counts[number] += 1
    for number in left:
        total += number * counts[number]
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

