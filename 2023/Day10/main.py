#!/usr/bin/env python3
import argparse

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)

UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

class Pipe:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.neighbors = set()
        self.connects_from = set()
        self.dist = float('inf')
        self.direction = 0
        self.str = '.'

        if type == '|':
            self.connects_from.add(UP)
            self.connects_from.add(DOWN)
            self.str = '┃'
        elif type == '-':
            self.connects_from.add(LEFT)
            self.connects_from.add(RIGHT)
            self.str = '━'
        elif type == 'L':
            self.connects_from.add(RIGHT)
            self.connects_from.add(UP)
            self.str = '┗'
        elif type == 'J':
            self.connects_from.add(UP)
            self.connects_from.add(LEFT)
            self.str = '┛'
        elif type == '7':
            self.connects_from.add(DOWN)
            self.connects_from.add(LEFT)
            self.str = '┓'
        elif type == 'F':
            self.connects_from.add(DOWN)
            self.connects_from.add(RIGHT)
            self.str = '┏'
        elif type == 'S':
            self.connects_from.add(UP)
            self.connects_from.add(DOWN)
            self.connects_from.add(LEFT)
            self.connects_from.add(RIGHT)
            self.dist = 0
            self.str = 'S'


    def make_connections(self, grid):
        for direction in self.connects_from:
            self.connect(direction, grid)


    def connect(self, direction, grid):
        try:
            if direction == UP:
                other = grid[self.y-1][self.x]
            elif direction == DOWN:
                other = grid[self.y+1][self.x]
            elif direction == LEFT:
                other = grid[self.y][self.x-1]
            elif direction == RIGHT:
                other = grid[self.y][self.x+1]
        except IndexError:
            return

        accepting_connector = (direction + 2) % 4
        if accepting_connector in other.connects_from:
            self.neighbors.add(other)

    def __str__(self):
        if self.direction < 0:
            color =' \033[0;31m'
        elif self.direction > 0:
            color =' \033[0;32m'
        else:
            color = ''
        return f'{color}{self.str}\033[0m'

    def __repr__(self):
        return str(self)


def part1(input_file):
    with open(input_file, 'r') as file:
        grid = []
        start = None
        for y,line in enumerate(file):
            row = []
            line = line.strip()
            for x,segment in enumerate(line):
                pipe = Pipe(segment, x, y)
                row.append(pipe)
                if segment == 'S':
                    start = pipe
            grid.append(row)

    for row in grid:
        for segment in row:
            segment.make_connections(grid)
        print(row)

    seen = set()
    fringe = []
    fringe.append(start)
    farthest = start
    while len(fringe) > 0:
        pipe = fringe.pop(0)
        if pipe.dist > farthest.dist:
            farthest = pipe
        for neighbor in pipe.neighbors:
            neighbor.dist = min(neighbor.dist, pipe.dist + 1)
            if neighbor not in seen and neighbor not in fringe:
                fringe.append(neighbor)
        seen.add(pipe)

    for row in grid:
        for segment in row:
            if segment in seen:
                print(segment, end='')
            else:
                print('.', end='')
        print()

    for row in grid:
        for segment in row:
            if segment in seen:
                print(segment.dist, end='')
            else:
                print('.', end='')
        print()

    return farthest.dist

def part2(input_file):
    with open(input_file, 'r') as file:
        grid = []
        start = None
        for y,line in enumerate(file):
            row = []
            line = line.strip()
            for x,segment in enumerate(line):
                pipe = Pipe(segment, x, y)
                row.append(pipe)
                if segment == 'S':
                    start = pipe
            grid.append(row)

    for row in grid:
        for segment in row:
            segment.make_connections(grid)
        print(row)

    seen = set()
    fringe = []
    fringe.append(start)
    farthest = start
    while len(fringe) > 0:
        pipe = fringe.pop(0)
        if pipe.dist > farthest.dist:
            farthest = pipe
        for neighbor in pipe.neighbors:
            neighbor.dist = min(neighbor.dist, pipe.dist + 1)
            if neighbor not in seen and neighbor not in fringe:
                fringe.append(neighbor)
        seen.add(pipe)

    last = start.neighbors.pop()
    node = start
    while True:
        for next in node.neighbors:
            if next != last:
                if node.y < next.y:
                    node.direction = 1
                    next.direction = 1
                elif next.y < node.y:
                    node.direction = -1
                    next.direction = -1
#                if last.y == node.y and last.direction == node.direction:
#                    node.direction = 0
                last = node
                node = next
                break
        if node == start:
            break


    for row in grid:
        for segment in row:
            if segment in seen:
                print(segment, end='')
            else:
                print('.', end='')
        print()

    for row in grid:
        for segment in row:
            if segment in seen:
                if segment.direction > 0:
                    print('+', end='')
                elif segment.direction < 0:
                    print('-', end='')
                else:
                    print('=', end='')
            else:
                print('.', end='')
        print()

    inside_count = 0
    for row in grid:
        count = 0
        last_direction = None
        for segment in row:
            if segment in seen:
                if segment.direction != last_direction:
                    count += segment.direction
                    if segment.direction != 0:
                        last_direction = segment.direction
                else:
                    segment.direction = 0
            else:
                if count % 2 == 0:
                    segment.type = 'O'
                    segment.str = 'O'
                else:
                    segment.type = 'I'
                    segment.str = 'I'
                    inside_count += 1

    result = []
    for row in grid:
        str_row = []
        for segment in row:
             str_row.append(str(segment).strip())
        result.append(''.join(str_row))
    print('\n'.join(result))

    return inside_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

#    print(part1(args.filename))
    print(part2(args.filename))

