#!/usr/bin/env python3
import re
import sys
import itertools

DEBUG=True


def dbg_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class Number:
    def __init__(self, value):
        self.value = value
        self.included = False


def part1(input_file):
    with open(input_file, 'r') as file:
        grid = []
        numbers = {}
        number_set = set()
        for y,line in enumerate(file):
            line = line.strip()
            grid.append(line)
            tokens = []
#            tokens = re.split(r'\D+',line)
#            tokens = line.split('.')

            i = 0
            while i < len(line):
                number = []
                start = i
                while i < len(line) and line[i].isdigit():
                    number.append(line[i])
                    i+=1
                if len(number) > 0:
                    print(number)
                    tokens.append((start, i, int(''.join(number))))
                    number = []
                i+=1
            for start, end, token in tokens:
#                print(f'{token} at ({x},{y}) through ({x+len(token)}, {y})')
                number = Number(int(token))
                number_set.add(number)
                for i in range(start,end):
                    numbers[(i, y)] = number

    total_ratio = 0
    for j,line in enumerate(grid):
        for i,c in enumerate(line):
            if c == '.' or c.isdigit():
                continue
            ratio = 1
            seen = set()
            for x,y in itertools.product([-1,0,1], [-1,0,1]):
                try:
                    number = numbers[(i+x,j+y)]
                    number.included = True
                    if number not in seen:
                        seen.add(number)
                        ratio *= number.value
                except KeyError:
                    pass
            if len(seen) == 2:
                seen = [ number.value for number in seen]
                total_ratio += ratio
                print(f'{c} is next to {seen}, so ratio is {ratio} for a total of {total_ratio}')


    result = []
    for i,row in enumerate(grid):
        print(row)
        line = []
        for j,c in enumerate(row):
            try:
                if numbers[(j,i)].included:
                    line.append('T')
                else:
                    line.append('F')
            except KeyError:
                line.append(c)
        result.append(''.join(line))
    print("\n\n=====\n\n")

    print('\n'.join(result))

    total = 0
    for number in number_set:
        if number.included:
            total += number.value

    return total,ratio



if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = "input.txt"
    print(part1(input_file))

