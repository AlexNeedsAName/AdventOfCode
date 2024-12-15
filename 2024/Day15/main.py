#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection

class Map:
    def __init__(self, width, height, walls, boxes, robot, double_wide):
        self.width = width
        self.height = height
        self.walls = walls
        self.boxes = boxes
        self.robot = robot
        self.double_wide = double_wide

    def try_move_box(self, point, direction, visited=None):
        if visited is None:
            visited = set()
        if point in visited:
            return True, set()

        if point in self.boxes:
            left_point = point
            right_point = point.move(CardinalDirection.EAST)
        elif point.move(CardinalDirection.WEST) in self.boxes:
            right_point = point
            left_point = point.move(CardinalDirection.WEST)
        elif point in self.walls:
            return False, None
        else:
            return True, set()


        # We know we're trying to move a box and what the left and right points of the box are
        # Add them to the visited set so any thing that checks the same box can just skip it
        visited.add(left_point)
        visited.add(right_point)

        if direction in (CardinalDirection.NORTH, CardinalDirection.SOUTH):
            # Moving up and down
            success, left_moved = self.try_move_box(left_point.move(direction), direction)
            if not success:
                return False, None
            success, right_moved = self.try_move_box(right_point.move(direction), direction)
            if not success:
                return False, None
            moved_boxes = left_moved.union(right_moved)
            moved_boxes.add(left_point)
            return True, moved_boxes

        if direction == CardinalDirection.EAST:
            point_to_move = right_point
        else:
            point_to_move = left_point

        success, moved_boxes = self.try_move_box(point_to_move.move(direction), direction)
        if not success:
            return False, None
        moved_boxes.add(left_point)
        return True, moved_boxes

    def move(self, direction):
        next = self.robot.move(direction)
        if next in self.walls:
            return False

        if self.double_wide:
            success, moved_boxes = self.try_move_box(next, direction)
            if success:
                self.boxes -= moved_boxes
                for box in moved_boxes:
                    self.boxes.add(box.move(direction))
            else:
                return False
        if next in self.boxes:
            pushed_into = next.move(direction)
            while True:
                if pushed_into in self.walls:
                    return False
                elif pushed_into in self.boxes:
                    pushed_into = pushed_into.move(direction)
                else:
                    self.boxes.remove(next)
                    self.boxes.add(pushed_into)
                    break
        self.robot = next
        return True


    def do_sequence(self, moves):
        dbg.print("Initial state:")
        dbg.print(self)
        dbg.print()
        for move in moves:
            dbg.print(f"Move {move.as_char()}:")
            self.move(move)
            dbg.print(self)
            dbg.print()


    def score(self):
        return sum(100 * box.y + box.x for box in self.boxes)


    @classmethod
    def from_file(cls, file, double_wide=False):
        grid = []
        walls = set()
        boxes = set()
        robot = set()
        width = 0
        height = 0
        for y,line in enumerate(file):
            line = line.strip()
            if len(line) == 0:
                break
            height = y
            if double_wide:
                new_line = []
                for c in line:
                    if c == 'O':
                        new_line.append('[]')
                    elif c == '@':
                        new_line.append('@.')
                    else:
                        new_line.append(f'{c}{c}')
                line = ''.join(new_line)
            grid.append([c for c in line])
            for x,c in enumerate(line):
                width = x
                p = Point(x,y)
                if c == '#':
                    walls.add(p)
                elif c == 'O' or c == '[':
                    boxes.add(p)
                elif c == "@":
                    robot = p

        width += 1
        height += 1
        return cls(width, height, walls, boxes, robot, double_wide)


    def __str__(self):
        lines = []
        for y in range(self.height):
            line = []
            skip = False
            for x in range(self.width):
                if skip:
                    skip = False
                    continue
                p = Point(x,y)
                if p in self.walls:
                    line.append('#')
                elif p in  self.boxes:
                    if not self.double_wide:
                        line.append('O')
                    else:
                        line.append('[')
                        line.append(']')
                        skip = True
                elif p == self.robot:
                    line.append('@')
                else:
                    line.append('.')
            lines.append(''.join(line))
        return '\n'.join(lines)


def problem(input_file, part2=False):
    inputs = []
    with open(input_file, 'r') as file:
        map = Map.from_file(file, double_wide=part2)
        for line in file:
            line = line.strip()
            for c in line:
                inputs.append(CardinalDirection.from_char(c))

    print(map)
    map.do_sequence(inputs)
    print(map)
    return map.score()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

