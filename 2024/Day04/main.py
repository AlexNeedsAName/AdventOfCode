#!/usr/bin/env python3
import argparse
from aoc_util import dbg
import re
from itertools import chain

class WordSearch():
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

    def get_horizontal(self, reverse=False):
#        print(f"Horizontal {'reverse' if reverse else ''}")
        if reverse:
            return (line[::-1] for line in self.grid)
        return self.grid

    def get_vertical(self, reverse=False):
#        print(f"Vertical {'reverse' if reverse else ''}")
        if reverse:
            return (line[::-1] for line in self.get_vertical())
        return (''.join(line[i] for line in self.grid) for i in range(self.width))

    # start bottom left going down and right
    def get_diagonals(self, downleft=False, reverse=False):
#        print(f"Diagonal {'down and left' if downleft else 'down and right'}")
        if reverse:
            return (line[::-1] for line in self.get_diagonals(downleft))
        result = []
        for row in reversed(range(self.height)):
#            print(f"Starting at row {row}")
            line = []
            for col in range(min(self.width, self.height - row)):
                if downleft:
                    real_col = -(col+1)
                else:
                    real_col = col
#                print(f"Reading row={row+col},{col=}")
                line.append(self.grid[row+col][real_col])
            result.append(''.join(line))
        for col in range(1,self.width):
#            print(f"Starting at col {col}")
            line = []
            for row in range(min(self.height, self.width-col)):
                real_col = row+col
                if downleft:
                    real_col = -(real_col+1)
#                print(f"Reading row={row},col={real_col}")
                line.append(self.grid[row][real_col])
            result.append(''.join(line))
        return result

    def all_directions(self):
#        return chain(self.get_horizontal(), self.get_horizontal(reverse=True), self.get_vertical(), self.get_vertical(reverse=True), self.get_diagonals(False), self.get_diagonals(True), self.get_diagonals(False, True), self.get_diagonals(True, True))
        return chain(self.get_horizontal(), self.get_vertical(), self.get_diagonals(False), self.get_diagonals(True))

    def diagonal_to_xy(self, i, j, downleft=False):
        return diagonal_to_xy(i, j, self.width, self.height, downleft)


def diagonal_to_xy(i,j, width, height, downleft=False):
    if i < height:
        x = j
        y = height-1 - i + j
    else:
        x = i-height + 1 + j
        y = j
    if downleft:
        x = width - 1 - x
#    print(f"{i=},{j=} -> {x=},{y=} ({downleft=})")
    return x, y


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)

    grid = WordSearch(lines)
    if not part2:
        total = 0
        for line in grid.all_directions():
            count = len(re.findall("(XMAS)", line))
            count_back = len(re.findall("(SAMX)", line))
            total += count + count_back
#            print(line, count, count_back, total)
        return total


    # Find the centers on both types of diagonals
    down_right_centers = []
    down_left_centers = []
    for i,line in enumerate(grid.get_diagonals()):
        down_right_centers.extend(grid.diagonal_to_xy(i, match.start()+1) for match in re.finditer("(MAS)", line))
        down_right_centers.extend(grid.diagonal_to_xy(i, match.start()+1) for match in re.finditer("(SAM)", line))
    for i,line in enumerate(grid.get_diagonals(downleft=True)):
        down_left_centers.extend(grid.diagonal_to_xy(i, match.start()+1, downleft=True) for match in re.finditer("(MAS)", line))
        down_left_centers.extend(grid.diagonal_to_xy(i, match.start()+1, downleft=True) for match in re.finditer("(SAM)", line))

    # Turn them into sets and find the intersection. Where the MAS's Cross
    down_right_centers = set(down_right_centers)
    down_left_centers = set(down_left_centers)
#    print(down_right_centers, down_left_centers)
    xmases = down_right_centers.intersection(down_left_centers)
    return len(xmases)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

