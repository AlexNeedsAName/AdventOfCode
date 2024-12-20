#!/usr/bin/env python3
import argparse
from aoc_util import dbg
import functools


sources = set()

@functools.cache
def is_possible(target):
    global sources
    if len(target) == 0:
        return True
    for prefix in sources:
        if target.startswith(prefix):
            print(f"{target} - {prefix} = {target[len(prefix):]}")
            if is_possible(target[len(prefix):]):
                return True
    return False

@functools.cache
def ways_to_make(target):
    global sources
    if len(target) == 0:
        return 1
    result = 0
    for prefix in sources:
        if target.startswith(prefix):
            print(f"{target} - {prefix} = {target[len(prefix):]}")
            result += ways_to_make(target[len(prefix):])
    return result

def problem(input_file, part2=False):
    global sources
    with open(input_file, 'r') as file:
        sources = set(file.readline().strip().split(', '))
        file.readline()
        targets = [line.strip() for line in file]

    if not part2:
        return sum(is_possible(target) for target in targets)
    return sum(ways_to_make(target) for target in targets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

