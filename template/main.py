#!/usr/bin/env python3
import argparse

DEBUG=0
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


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
    DEBUG = args.verbose

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

