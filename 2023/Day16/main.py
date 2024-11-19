#!/usr/bin/env python3
import argparse
from collections import deque as queue
from aoc_util import dbg_print, RelativeDirection, CardinalDirection, Point
import time

def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class Lazer:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def get_next(self, tile):
        if tile in ['/', '\\']:
            direction = self.direction.mirror(tile)
            return [Lazer(self.position.move(direction), direction)]
        elif tile == '-' and self.direction.is_vertical():
            return [Lazer(self.position.move(d), d) for d in (CardinalDirection.EAST, CardinalDirection.WEST)]
        elif tile == '|' and self.direction.is_horizontal():
            return [Lazer(self.position.move(d), d) for d in (CardinalDirection.NORTH, CardinalDirection.SOUTH)]
        else:
            return [Lazer(self.position.move(self.direction), self.direction)]

    def __repr__(self):
        return(f"Lazer({self.position}, {self.direction})")

    def __hash__(self):
        return hash((self.position.x, self.position.y, self.direction))

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction


class Board:
    def __init__(self, board):
        self.board = board
        self.height = len(self.board)
        self.width = len(self.board[0])
        #self.energized = [['.' for i in range(self.width)] for j in range(self.height)]

        dbg_print(f"{self.height=} {self.width=} {self.board[0]=}")

    def energize(self, initial_lazers, destructive=False):
        frontier = queue(initial_lazers)
        seen = set()
        energized = set()

        # Use none's to keep track of one time step
        global DEBUG
        if DEBUG > 0:
            frontier.append(None)

        while len(frontier) > 0:
            lazer = frontier.popleft()

            if lazer is None:
                if DEBUG > 0:
                    dbg_print(self, level=2)
                    dbg_print("\n================================================\n", level=2)
                    time.sleep(.1)
                if len(frontier) > 0:
                    frontier.append(None)
                continue

            seen.add(lazer)
            energized.add(lazer.position)
            dbg_print(f"Processing lazer {lazer}", level=3)
            #self.energized[lazer.position.y][lazer.position.x] = '#'
            tile = self.at(lazer.position)
            if destructive:
                if tile == '.':
                    self.set(lazer.position, lazer.direction.as_char())
                elif tile in "^v<>":
                    self.set(lazer.position, '2')
                elif tile in "23456789":
                    tile = str(int(tile)+1)

            sucessors = lazer.get_next(self.at(lazer.position))
            dbg_print(sucessors, level=3)
            for sucessor in sucessors:
#                if sucessor in seen:
#                    print("Skipping because seen")
#                elif 0 > sucessor.position.x:
#                    print("Skipping because x too small")
#                elif 0 > sucessor.position.y:
#                    print("Skipping because y too small")
#                elif sucessor.position.x >= self.width:
#                    print(f"Skipping because x too big (position {sucessor.position.x} >= width {self.width})")
#                elif sucessor.position.y >= self.height:
#                    print("Skipping because y too big")
#                else:
#                    frontier.append(sucessor)
                if 0 <= sucessor.position.x < self.width and 0 <= sucessor.position.y < self.height and sucessor not in seen:
                    frontier.append(sucessor)

        return energized

    def at(self, position):
        return self.board[position.y][position.x]

    def set(self, position, char):
        self.board[position.y][position.x] = char

    @classmethod
    def from_file(cls, file):
        board = [list(line.strip()) for line in file]
        return cls(board)

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.board)


    def show_energized(self, energized_positions):
        energized = [['#' if Point(x,y) in energized_positions else '.' for x in range(self.width)] for y in range(self.height)]
        print('\n'.join(''.join(line) for line in energized))


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        board = Board.from_file(file)

    if not part2:
        energized_positions = board.energize([Lazer(Point(0,0), CardinalDirection.EAST)], destructive=True)
        print(board)
        board.show_energized(energized_positions)
        return len(energized_positions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose
    print(f"DEBUG is {DEBUG}")

    print(problem(args.filename))
#    print(problem(args.filename, part2=True))

