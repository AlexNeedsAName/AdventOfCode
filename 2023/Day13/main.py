#!/usr/bin/env python3
import argparse
import functools

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class Cols:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = [row[self.index] for row in self.data]
            self.index += 1
            return row
        except IndexError:
            raise StopIteration

def transpose(matrix):
    return [row for row in Cols(matrix)]


def distance(A, B):
    return sum(0 if a==b else 1 for a,b in zip(A,B))


def differences(A,B):
    return [i for i,(a,b) in enumerate(zip(A,B)) if a != b]


def is_horizontal_reflection(data, row, smudge_count=0):
    total_dist = 0
    left = data[:row][::-1]
    right = data[row:]
    dbg_print(f'Checking if row {row} is a line of reflection with {smudge_count} smudges', level=2)
    dbg_print('\n'.join(left[::-1] + [('-' * len(data[0]))] + right), level=2)
    for i, (a,b) in enumerate(zip(left, right)):
        total_dist += distance(a,b)
        if total_dist > smudge_count:
            dbg_print('', level=2)
            return False
    dbg_print(f'Total dist is {total_dist}\n', level=2)
    return total_dist == smudge_count


def is_horizontal_reflection_no_smudges(data, row):
    left = data[:row][::-1]
    right = data[row:]
    dbg_print(f'Checking if row {row} is a line of reflection', level=2)
    dbg_print('\n'.join(left[::-1] + [('-' * len(data[0]))] + right), level=2)
    for a,b in zip(left, right):
        if a != b:
            dbg_print('')
            return False
    dbg_print('It is!\n')
    return True


#def is_vertical_reflection(data, col):
#    return is_horizontal_reflection([''.join(line) for line in transpose(data)], col)


digits = [str(i) for i in range(1,10)] + [chr(c) for c in range(ord('A'), ord('Z')+1)]

class Map:
    def __init__(self, data, smudge_count):
        self.data = data
        self.vertical_reflections = []
        self.horizontal_reflections = []

        smudge_rows = {}
        smudge_cols = {}
        for i in range(1,len(self.data)):
            if is_horizontal_reflection(data, i, smudge_count):
                self.horizontal_reflections.append(i)

        transposed = [''.join(row) for row in transpose(self.data)]
        for i in range(1,len(transposed)):
            if is_horizontal_reflection(transposed, i, smudge_count):
                self.vertical_reflections.append(i)

        dbg_print(self)
        dbg_print(f'\nHorizontal Reflections: {self.horizontal_reflections}')
        dbg_print(f'Vertical Reflections: {self.vertical_reflections}\n')


    @classmethod
    def from_file(cls, file):
        data = []
        for line in file:
            line = line.strip()
            print(line)
            if len(line) == 0:
                break
            data.append(line)
        if len(data) == 0:
            result = None
        else:
            result =  cls(data)
        print(result)
        return result

    def value(self):
        return sum(100 * self.horizontal_reflections) + sum(self.vertical_reflections)

    def __str__(self):
        results = []
        if len(self.horizontal_reflections) > 0:
            pad = '  '
        else:
            pad = ''
        width = len(self.data[0])

        if len(self.vertical_reflections) > 0:
            results.append(pad + ''.join(digits[:width]))
            line = [' '] * width
            for col in self.vertical_reflections:
                line[col-1] = '>'
                line[col] = '<'
            results.append(pad + ''.join(line))

        if len(self.horizontal_reflections) > 0:
            for i,line in enumerate(self.data):
                indicator = ' '
                if i+1 in self.horizontal_reflections:
                    indicator = 'v'
                elif i in self.horizontal_reflections:
                    indicator = '^'
                results.append(f'{digits[i]}{indicator}{line}{indicator}{digits[i]}')
        else:
            results.extend([pad + row for row in self.data])

        if len(self.vertical_reflections) > 0:
            results.append(results[1])
            results.append(results[0])
        return '\n'.join(results)


def problem(input_file, part2=False):
    maps = []
    total = 0
    smudge_count = 1 if part2 else 0
    with open(input_file, 'r') as file:
        data = []
        for line in file:
            line = line.strip()
            if len(line) == 0:
                total += Map(data, smudge_count).value()
                data = []
            else:
                data.append(line)
        if len(data) > 1:
            total += Map(data, smudge_count).value()

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

