#!/usr/bin/env python3
import argparse
from aoc_util import dbg

def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

def concat(a,b):
    return int(str(a)+str(b))

def can_be_made(test, operands, operators):
    if len(operands) == 1:
        return test == operands[0]
    for op in operators:
        if can_be_made(test, [op(operands[0], operands[1])] + operands[2:], operators):
            return True
    return False

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            test, operands = line.split(':')
            test = int(test)
            operands = [int(token) for token in operands.strip().split()]
            lines.append((test, operands))

    total = 0
    operators = [add, multiply]
    if part2:
        operators.append(concat)
    for test,operands in lines:
        if can_be_made(test, operands, operators):
            total += test
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

