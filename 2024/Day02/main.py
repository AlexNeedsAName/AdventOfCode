#!/usr/bin/env python3
import argparse
from aoc_util import dbg

def is_safe(report):
    is_ascending = True
    is_descending = True
    for a,b in zip(report, report[1:]):
        if a > b:
            is_ascending = False
        elif b > a:
            is_descending = False
        if 3 >= abs(a-b) >= 1:
            pass
        else:
            return False
    return is_ascending or is_descending

def is_safe_damped(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False

def problem(input_file, part2=False):
    reports = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            reports.append([int(element) for element in line.split()])
    if not part2:
        return sum(is_safe(report) for report in reports)
    return sum(is_safe_damped(report) for report in reports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

