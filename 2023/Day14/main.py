#!/usr/bin/env python3
import argparse
from enum import Enum
import copy

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Cols:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        row = [row[self.index] for row in self.data]
        self.index += 1
        return row


def transpose(matrix):
    return [row for row in Cols(matrix)]


def shift_left(line):
    line = line.copy()
    count = 0
    for i,c in enumerate(line):
        if c == 'O':
            count += 1
            for j in range(i,0,-1):
                if line[j-1] == '.':
                    line[j-1] = 'O'
                    line[j] = '.'
                else:
                    break
    return line


class Board:
    def __init__(self, data):
        self.data = data

    def tilt(self, direction):
        new_data = []

        dbg_print(f'Tilting {direction}')

        if direction == Direction.NORTH:
            for col in Cols(self.data):
                new_data.append(shift_left(col))
            new_data = transpose(new_data)
        elif direction == Direction.SOUTH:
            for col in Cols(self.data):
                new_data.append(shift_left(col[::-1])[::-1])
            new_data = transpose(new_data)
        elif direction == Direction.WEST:
            new_data = [shift_left(row) for row in self.data]
        elif direction == Direction.EAST:
            new_data = [shift_left(row[::-1])[::-1] for row in self.data]
        else:
            raise ValueError(f'Invalid direction {direction}')

        return Board(new_data)

    def cycle(self, count=1):
        i = 0
        result = self
        board_to_index = {}
        index_to_board = {}
        while i < count:
            if result in board_to_index.keys():
                cycles_after = board_to_index[result]
                cycle_length = i-cycles_after
                print(f"cycle found! Starts at {cycles_after} with a length of {cycle_length}")
                remaining = count - i
                result = index_to_board[cycles_after + remaining % cycle_length]
                break
            else:
                board_to_index[result] = i
                index_to_board[i] = result
                for direction in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
                    dbg_print(result)
                    result = result.tilt(direction)
            i += 1

        return result

    def load(self):
        return sum(row.count('O') * (len(self.data)-i) for i,row in enumerate(self.data))

    @classmethod
    def from_file(cls, file):
        data = []
        for line in file:
            data.append([c for c in line.strip()])
        return cls(data)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.data)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        board = Board.from_file(file)

    if not part2:
        board = board.tilt(Direction.NORTH)
    else:
        board = board.cycle(1000000000)

    print(board)
    return board.load()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

