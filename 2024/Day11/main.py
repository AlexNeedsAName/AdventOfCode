#!/usr/bin/env python3
import argparse
from aoc_util import dbg
import functools

def blink(stones):
    i = 0
    while i < len(stones):
        stone = stones[i]
        if stone == 0:
            stones[i] = 1
            i += 1
            continue

        str_stone = str(stone)
        digits = len(str_stone)
        if digits % 2 == 0:
            half = digits//2
            left, right = int(str_stone[:half]), int(str_stone[half:])
            stones[i] = left
            stones.insert(i+1, right)
            i += 2
            continue

        stones[i] = stone * 2024
        i += 1

@functools.cache
def blink_stone(stone, count):
    if count == 0:
        return 1

    if stone == 0:
        return blink_stone(1, count-1)

    str_stone = str(stone)
    digits = len(str(stone))
    if digits % 2 == 0:
        half = digits//2
        left, right = int(str_stone[:half]), int(str_stone[half:])
        return blink_stone(left, count-1) + blink_stone(right, count-1)

    return blink_stone(stone * 2024, count-1)


def blink_fast(stones, count):
    total = 0
    for stone in stones:
        total += blink_stone(stone, count)
    return total

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        for line in file:
            stones = [int(token) for token in line.strip().split()]

        dbg.print("Initial arrangement:")
        if not part2:
            count = 25
        else:
            count = 75

#        for i in range(count):
#            dbg.print(stones)
#            blink(stones)
#            print(f"After {i} blink{'s' if i > 1 else ''}, there are {len(stones)} stones")
#        dbg.print(stones)
#
#    return len(stones)

    return blink_fast(stones, count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

