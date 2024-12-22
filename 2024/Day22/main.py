#!/usr/bin/env python3
import argparse
from aoc_util import dbg
import itertools
from collections import defaultdict

class CircularArray:
    def __init__(self, maxsize):
        self.size = 0
        self.maxsize = maxsize
        self.data = [None for i in range(maxsize)]
        self.i = 0

    def add(self, value):
        self.data[self.i] = value
        self.i = (self.i+1) % self.maxsize

    def last(self):
        return self.data[(self.i+self.maxsize-1) % self.maxsize]

    def as_tuple(self):
        return (*self.data[self.i:], *self.data[:self.i])

def mix(number, secret):
    return number ^ secret

def prune(number):
    return number % 16777216

def evolve(number):
    number = prune(mix(number * 64, number))
    number = prune(mix(number // 32, number))
    number = prune(mix(number * 2048, number))
    return number

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        numbers = [int(line.strip()) for line in file]


    if part2:
        size = 4
        sequences = itertools.product(range(-9,10), repeat=size)
#        print([sequence for sequence in sequences])

        results = defaultdict(lambda: defaultdict(lambda: None))
        for i,number in enumerate(numbers):
            init = number
            last = init % 10
            changes = CircularArray(size)
            for j in range(2000):
                number = evolve(number)
                price = number % 10
                changes.add(price - last)
                dbg.print(f"{number}: {price} {changes.last()}")
                if j >= 4:
                    seq = changes.as_tuple()
                    if results[seq][i] is None:
                        results[seq][i] = price
                last = price

        best = 0
        for result in results.values():
            total = sum(v for v in result.values() if v is not None)
            if total > best:
                best = total
        return best

    total = 0
    for number in numbers:
        init = number
        dbg.print(f"{number=}", level=2)
        for i in range(2000):
            number = evolve(number)
            dbg.print(number, level=2)
        dbg.print(level=2)
        dbg.print(f"{init}: {number}")
        total += number

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

