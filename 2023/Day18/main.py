#!/usr/bin/env python3
import argparse
from enum import Enum
from progressbar import progressbar

DEBUG=0
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class CardinalDirection(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn(self, relative_direction):
        return CardinalDirection((self.value + relative_direction.value) % 4)

    def as_char(self):
        if self == CardinalDirection.NORTH:
            return '^'
        elif self == CardinalDirection.EAST:
            return '>'
        elif self == CardinalDirection.SOUTH:
            return 'v'
        elif self == CardinalDirection.WEST:
            return '<'

    @staticmethod
    def from_char(char):
        if char == 'U' or char == 'N':
            return CardinalDirection.NORTH
        elif char == 'D' or char == 'S':
            return CardinalDirection.SOUTH
        elif char == 'L' or char == 'W':
            return CardinalDirection.WEST
        elif char == 'R' or char == 'E':
            return CardinalDirection.EAST

    def move(self, point):
        x,y = point
        if self == CardinalDirection.NORTH:
            y -= 1
        elif self == CardinalDirection.EAST:
            x += 1
        elif self == CardinalDirection.SOUTH:
            y += 1
        elif self == CardinalDirection.WEST:
            x -= 1
        return (x,y)


class Trench:
    def __init__(self, compressed=True):
        self.board = [['.']]
        self.position = (0,0)
        self.compressed = compressed


    def _add_row(self, index=None):
        if index is None:
            index = len(self.board)
        self.board.insert(index, ['.'] * len(self.board[0]))

    def _add_col(self, index=None):
        if index is None:
            index = len(self.board[0])
        for row in self.board:
            row.insert(index, '.')

    def dig(self, direction, count):
        x,y = self.position
        c = direction.as_char()
#        c = '#'
        if not self.compressed:
            for i in range(count):
                if direction == CardinalDirection.NORTH:
                    self.board[y][x] = c
                    y -= 1
                elif direction == CardinalDirection.SOUTH:
                    self.board[y][x] = c
                    y += 1
                elif direction == CardinalDirection.EAST:
                    x += 1
                elif direction == CardinalDirection.WEST:
                    x -= 1


                if y < 0:
                    self._add_row(0)
                    y += 1
                elif y >= len(self.board):
                    self._add_row()
                elif x < 0:
                    self._add_col(0)
                    x += 1
                elif x >= len(self.board[0]):
                    self._add_col()

                self.board[y][x] = c

        dbg_print((x,y))
        dbg_print(self, end='\n\n')

        self.position = (x,y)

    def dig_inside(self):
        self._add_col()
        for y,line in enumerate(self.board):
            count = 0
            last_seen = None
            in_line = False
            for x,(tile,next) in enumerate(zip(line, line[1:])):
#                if in_line and tile in '<>':
#                    self.board[y][x] = '-'
                if in_line and next == '.':
                    in_line = False
                    if last_seen == tile:
                        self.board[y][x] = '#'
                        continue

                if tile == '^':
                    if next != '.':
                        last_seen = '^'
                        in_line = True
                    count += 1
                elif tile == 'v':
                    if next != '.':
                        last_seen = 'v'
                        in_line = True
                    count -= 1
#                if count != 0 and tile == '.':
#                    self.board[y][x] = str(abs(count))
                if count != 0 or tile != '.':
                    self.board[y][x] = '#'
            line.pop()


    def volume(self):
        return str(self).count('#')

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.board)

def problem(input_file, part2=False):
#    trench = Trench(compressed=part2)
    trench = Trench(compressed=True)
    with open(input_file, 'r') as file:
        for line in progressbar(file.readlines()):
            direction, dist, color = line.split()
            color = color[1:-1] # remove parens
            if not part2:
                trench.dig(CardinalDirection.from_char(direction), int(dist))
            else:
                color = color[1:] # remove the #
                dist = int(color[:5], 16)
                direction = CardinalDirection((int(color[-1])+1) % 4)
                trench.dig(direction, dist)
    print(trench, end='\n\n')
    print("Done digging trench")
    trench.dig_inside()
    print("Done digging out the inside of the trench")
    print(trench, end='\n\n')
    return trench.volume()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(problem(args.filename))
#    print(problem(args.filename, part2=True))

