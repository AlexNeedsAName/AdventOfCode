#!/usr/bin/env python3
import argparse
import itertools

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)

def taxicab(A, B):
    return sum(abs(a-b) for a,b in zip(A,B))

class Galaxy:
    def __init__(self, data):
        self.data = data

    def get_galaxies(self):
        results = []
        for i,row in enumerate(self.data):
            for j,value in enumerate(row):
                if value == '#':
                    results.append((i,j))
        return results

    def empty_rows(self):
        indicies = []
        for i,row in enumerate(self.data):
            if '#' not in row:
                indicies.append(i)
        return indicies

    def expand_rows(self, indicies):
        for i,j in enumerate(indicies):
            self.data.insert(i+j, self.data[i+j])

    def empty_cols(self):
        indicies = []
        for col in range(len(self.data[0])):
            empty = True
            for row in self.data:
                if row[col] == '#':
                    empty = False
                    break
            if empty:
                indicies.append(col)

        return indicies

    def expand_cols(self, indicies):
        for i,j in enumerate(indicies):
            for row in self.data:
                row.insert(i+j, '.')

    def expand(self):
        rows = self.empty_rows()
        cols = self.empty_cols()

        # ====================================
        width = len(self.data[0])
        line = [' '] * (width + 1)
        line2 = [' '] * (width + 1)
        for col in cols:
            line[col+1] = 'V'
            line2[col+1] = '^'
        dbg_print(''.join(line))
        for i,row in enumerate(self.data):
            line = []
            if i in rows:
                line.append('>')
            else:
                line.append(' ')
            line.extend(row)
            if i in rows:
                line.append('<')
            else:
                line.append(' ')
            dbg_print(''.join(line))
        dbg_print(''.join(line2))
        # ====================================

        self.expand_cols(cols)
        self.expand_rows(rows)

        dbg_print('\n')
        dbg_print(str(self))

    def taxicab_pairs(self, expansion=0):
        rows = self.empty_rows()
        cols = self.empty_cols()
        dbg_print(f'rows: {rows}')
        dbg_print(f'cols: {cols}')
        galaxies = []
        for galaxy in self.get_galaxies():
            row, col = galaxy
            dbg_print(row,col)
            row += sum([1 if v < row else 0 for v in rows]) * (expansion-1)
            col += sum([1 if v < col else 0 for v in cols]) * (expansion-1)
            print(row, col)
            galaxies.append((row,col))

        dbg_print(f'galaxies: {galaxies}')

        distances = []
        for pair in itertools.combinations(galaxies, 2):
            distances.append(taxicab(*pair))
        return sum(distances)

    @classmethod
    def from_file(cls, file):
        data = []
        for line in file:
            data.append([char for char in line.strip()])
        return cls(data)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.data)


def part1(input_file):
    with open(input_file, 'r') as file:
        galaxy = Galaxy.from_file(file)
    galaxy.expand()
    return galaxy.taxicab_pairs()


def part2(input_file):
    with open(input_file, 'r') as file:
        galaxy = Galaxy.from_file(file)
#    dbg_print(f'expansion = 10: {galaxy.taxicab_pairs(10)}')
#    dbg_print(f'expansion = 100: {galaxy.taxicab_pairs(100)}')
#    dng_print(f'expansion = 1000000: {galaxy.taxicab_pairs(1000000)}')
    return galaxy.taxicab_pairs(1000000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))
    print(part2(args.filename))

