#!/usr/bin/env python3
import argparse
from aoc_util import dbg


def problem(input_file, part2=False):
    masses = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            masses.append(int(line))

    if not part2:
        return sum(mass // 3 - 2 for mass in masses)
    required_fuel = 0
    for mass in masses:
        while True:
            fuel = mass // 3 - 2
            if fuel <= 0:
                break
            required_fuel += fuel
            mass = fuel
    return required_fuel


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

