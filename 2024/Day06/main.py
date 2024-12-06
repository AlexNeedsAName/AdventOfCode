#!/usr/bin/env python3
import argparse
from aoc_util import dbg, CardinalDirection, RelativeDirection, Point

class Board:
    def __init__(self, grid, pos, direction):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.starting_pos = pos
        self.starting_direction = direction
        self.reset()

    @classmethod
    def from_file(cls, file):
        grid = []
        pos = None
        for y,line in enumerate(file):
            line = line.strip()
            if '^' in line:
                pos = Point(line.index('^'), y)
            grid.append([c for c in line])
        x,y = pos
        grid[y][x] = '.'
        return cls(grid, pos, CardinalDirection.NORTH)

    def __str__(self):
#        return ''.join(''.join(line for line in self.grid))
        result = []
        for y,line in enumerate(self.grid):
            result_line = []
            for x,c in enumerate(line):
                p = Point(x,y)
                if p == self.pos:
                    result_line.append(self.direction.as_char())
                elif p in self.visited_spaces:
                    result_line.append('X')
                else:
                    result_line.append(c)
            result.append(''.join(result_line))
        return '\n'.join(result)

    def walk(self):
        while True:
            next_pos = self.pos.move(self.direction)
            if not self.in_bounds(next_pos):
                self.pos = next_pos
                return False
            elif self.grid[next_pos.y][next_pos.x] == '#' or next_pos == self.test_obstacle:
                self.direction = self.direction.turn(RelativeDirection.RIGHT)
                if (self.pos, self.direction) in self.visited:
                    return False
                self.visited.add((self.pos, self.direction))
                return True
            self.pos = next_pos
            self.visited.add((self.pos, self.direction))
            self.visited_spaces.add(self.pos)

    def walk_off(self):
        in_bounds = True
        while in_bounds:
            in_bounds = self.walk()
            dbg.print(self,'\n')

    def in_bounds(self, position=None):
        if position is None:
            position = self.pos
        return not (position.x < 0 or position.x >= self.width or position.y < 0 or position.y >= self.height)

    def reset(self):
        self.pos = self.starting_pos
        self.direction = self.starting_direction
        self.visited = set((self.pos,self.direction))
        self.visited_spaces = set((self.pos,))
        self.test_obstacle = Point(-1,-1)

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        board = Board.from_file(file)
    dbg.print(board)
    board.walk_off()
    if not part2:
        return len(board.visited)

    loop_points = set()
    test_locations = board.visited_spaces
    for point in test_locations:
        if point == board.starting_pos:
            continue
        board.reset()
        board.test_obstacle = point
        board.walk_off()
        if board.in_bounds():
            loop_points.add(point)
    return len(loop_points)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))

