#!/usr/bin/env python3
import argparse
from aoc_util import dbg


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        for line in file:
            numbers = [int(c) for c in line.strip()]
    print(numbers)

    is_file = True
    id = 0
    ids = []
    gaps = []
    expanded = []
    for number in numbers:
        if is_file:
            ids.append((len(expanded), number, id))
            expanded.extend([id] * number)
            id += 1
        else:
            gaps.append((len(expanded), number))
            expanded.extend(['.'] * number)
        is_file = not is_file

    print(''.join(str(x) for x in expanded))

    if not part2:
        i = 0
        j = len(expanded)-1
        while i < j:
#            print(''.join(str(x) for x in expanded))
            if expanded[i] == '.':
                expanded[i] = expanded[j]
                expanded[j] = '.'
                while expanded[j] == '.' and i < j:
                    j-=1
            i+=1
        expanded = expanded[:j+1]

    else:
        for file_start_index, file_size, file in reversed(ids):
#            print(''.join(str(x) for x in expanded))
            for gap_index,(gap_start_index, gap_size) in enumerate(gaps):
                if gap_start_index >= file_start_index:
                    break
                if gap_size >= file_size:
                    for i in range(file_size):
                        expanded[gap_start_index+i] = file
                        expanded[file_start_index+i] = '.'
                    gap_size -= file_size
                    gap_start_index += file_size
                    if gap_size == 0:
                        gaps.pop(gap_index)
                    else:
                        gaps[gap_index] = (gap_start_index, gap_size)
                    break

    print(''.join(str(x) for x in expanded))

    if part2:
        for i in range(len(expanded)):
            if expanded[i] == '.':
                expanded[i] = 0

    return sum(num*pos for pos,num in enumerate(expanded))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

