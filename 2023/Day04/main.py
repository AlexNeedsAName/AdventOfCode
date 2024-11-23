#!/usr/bin/env python3
import sys

DEBUG=True


def dbg_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)



def part1(input_file):
    with open(input_file, 'r') as file:
        sum = 0
        for line in file:
            line = line.strip()
            card_str, winning_str = line.split('|')
            winning = set()
            for number in winning_str.split(' '):
                if len(number) == 0:
                    continue
                winning.add(int(number))
            card_str = card_str.split(':')[-1]
            count = 0
            for number in card_str.split(' '):
                if len(number) == 0:
                    continue
                number = int(number)
                if number in winning:
                    count += 1
            if count > 0:
                sum += 2**(count-1)
    return sum

def part2(input_file):
    with open(input_file, 'r') as file:
        cards = 0
        copies = []
        for line in file:
            copies_of_this = 1
            if len(copies) > 0:
                copies_of_this += copies.pop(0)
            cards += copies_of_this

            line = line.strip()
            card_str, winning_str = line.split('|')
            winning = set()
            for number in winning_str.split(' '):
                if len(number) == 0:
                    continue
                winning.add(int(number))
            card_str = card_str.split(':')[-1]
            count = 0
            for number in card_str.split(' '):
                if len(number) == 0:
                    continue
                number = int(number)
                if number in winning:
                    count += 1
            if count > 0:
                for i in range(count):
                    try:
                        copies[i] += copies_of_this
                    except IndexError:
                        copies.append(copies_of_this)
    return cards


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = "input.txt"
    print(part1(input_file))
    print(part2(input_file))

