#!/usr/bin/env python3
import argparse
from aoc_util import dbg


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            pass
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

