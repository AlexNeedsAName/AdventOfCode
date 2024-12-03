#!/usr/bin/env python3
import argparse
from aoc_util import dbg
import re

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
    full_input = '\n'.join(lines)
    result = re.findall("(mul\([\d]*,[\d]*\)|do\(\)|don't\(\))", full_input)
    total = 0
    enabled = True
    for command in result:
        if command.startswith("don't"):
            enabled = False
        elif command.startswith("do"):
            enabled = True
        elif (not part2 or enabled) and command.startswith("mul"):
            command = command[4:-1]
            x,y = command.split(',')
            total += int(x) * int(y)
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

