#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection
#import search
import astar
import functools


class Memory:
    def __init__(self, unsafe, width=None, height=None):
        if width is None or height is None:
            found_width = -1
            found_height = -1
            for x,y in unsafe:
                if x > found_width:
                    found_width = x
                if y > found_height:
                    found_height = y
            found_width += 1
            found_height += 1
            if width is None:
                width = found_width
            if height is None:
                height = found_height

        self.width = width
        self.height = height
        self.unsafe = unsafe


    @functools.cache
    def fallen_spaces_after(self, n):
        return set(self.unsafe[:n+1])


    def str_after(self, n=None, path=None, cross=None):
        if n is None:
            unsafe_set = set(self.unsafe)
        else:
            unsafe_set = self.fallen_spaces_after(n)
        if path is None:
            path = set()
        result = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = Point(x,y)
                if p == cross:
                    line.append('X')
                elif p in unsafe_set:
                    line.append('#')
                elif p in path:
                    line.append('O')
                else:
                    line.append('.')
            result.append(''.join(line))
        return '\n'.join(result)


    def __str__(self):
        return self.str_after()


    @classmethod
    def from_file(cls, file, width=None, height=None):
        unsafe = list()
        for line in file:
            p = Point(*(int(token) for token in line.strip().split(',')))
            unsafe.append(p)
        return cls(unsafe, width, height)


class StaticMemorySearch(astar.AStar):
    def __init__(self, memory, time):
        self.memory = memory
        self.time = time


    def neighbors(self, position):
        result = []
        for direction in CardinalDirection:
            next = position.move(direction)
            if next in self.memory.fallen_spaces_after(self.time) or next.x < 0 or next.y < 0 or next.x >= self.memory.width or next.y >= self.memory.height:
                continue
            result.append(next)
        return result


    def distance_between(self, p1, p2):
        return 1


    def heuristic_cost_estimate(self, current, goal):
        x1,y1 = current
        x2,y2 = goal
        return abs(x1-x2)+abs(y1-y2)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        mem = Memory.from_file(file)

    time = 1024
    end = Point(70,70)
    if input_file == "small.txt":
        time = 12
        end = Point(6,6)

    print(mem.str_after(time))
    print(mem.width, mem.height)
    path_list = list(StaticMemorySearch(mem, time).astar(Point(0,0), end))
    if not part2:
        print(mem.str_after(time, path_list))
        return len(path_list) - 1

    path = set(path_list)
    time += 1
    while time <=len(mem.unsafe):
        new_block = mem.unsafe[time]
        if new_block in path_list:
            # The falling memory blocked our path, find a new one if we still can
            path = StaticMemorySearch(mem, time).astar(Point(0,0), end)
            if path is None:
                partial_path = []
                for p in path_list:
                    if p == new_block:
                        break
                    partial_path.append(p)
                print(mem.str_after(time, partial_path, new_block))
                return new_block
            path_list = list(path)
            path = set(path_list)
            print(mem.str_after(time, path))
            print()
        time += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))


