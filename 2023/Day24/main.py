#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point2d, Point3d
import numpy as np
from itertools import combinations

class Line:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    @classmethod
    def from_point_slope(cls, point, slope):
        m = slope
        b = point.y - slope * point.x
        return cls(m, b)

    @classmethod
    def from_point_vel(cls, point, vel):
        return cls.from_point_slope(point, vel.y / vel.x)

    def at(self, x):
        return self.m * x + self.b

    def intersects(self, other):
        if self.m == other.m:
            if self.b == other.b:
                return True # intersects everywhere
            else:
                return False #intersects nowhere
        x = (other.b - self.b) / (self.m - other.m)
        y = self.at(x)
        return Point2d(x,y)

class Hailstone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.line = Line.from_point_vel(position, velocity)

    @classmethod
    def from_line(cls, line):
        pos, vel = line.split('@')
        pos = Point3d(*(int(v) for v in pos.strip().split(',')))
        vel = Point3d(*(int(v) for v in vel.strip().split(',')))
        return cls(pos,vel)

    def at(self, t):
        return Point3d(self.position.x + self.velocity.x * t, self.position.y + self.velocity.y * t, self.position.z + self.velocity.z * t)

    def crosses_within(self, other, min, max):
        dbg.print(f'\nHailstone A: {self}')
        dbg.print(f'Hailstone B: {other}')
        intersects = self.line.intersects(other.line)
        if intersects == False:
            dbg.print("Hailstones' paths are parallel; they never interact")
            return False
        elif intersects == True:
            dbg.print("Hailstones' paths are parallel; they follow the same path")
            return False

        x,y = intersects
        if x < min or x > max or y < min or y > max:
            dbg.print(f"Hailstones' paths will cross outside the test area (at x={x}, y={y})")
            return False
        elif (x > self.position.x and self.velocity.x < 0) or (x < self.position.x and self.velocity.x > 0):
            dbg.print("Hailstones' paths crossed in the past for hailstone A.")
            return False
        elif (x > other.position.x and other.velocity.x < 0) or (x < other.position.x and other.velocity.x > 0):
            dbg.print("Hailstones' paths crossed in the past for hailstone B.")
            return False

        dbg.print(f"Hailstones' paths will cross \033[1minside\033[0m the test area at (at x={x}, y={y})")
        return True


    def __str__(self):
        return f'{self.position} @ {self.velocity}'


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        storm = [Hailstone.from_line(line) for line in file]

    if not part2:
        total = 0
        for A,B in combinations(storm, 2):
    #        if A.crosses_within(B, 7, 27):
            if A.crosses_within(B, 200000000000000, 400000000000000):
                total += 1
        return total

    # Part 2
    # Using the neat cross product trick from https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kxqjg33/
    (p1,v1), (p2,v2), (p3,v3) = ((stone.position, stone.velocity) for stone in storm[:3])
    print(f"{p1=}; {p2=}; {p3=}")
    print(f"{v1=}; {v2=}; {v3=}")
    p1 -= p3
    p2 -= p3
    v1 -= v3
    v2 -= v3
    print(f"{p1=}; {p2=};")
    print(f"{v1=}; {v2=};")
    t1 = -(p1.cross(p2) * v2) / (v1.cross(p2) * v2)
    t2 = -(p1.cross(p2) * v1) / (p1.cross(v2) * v1)
    c1 = (p1+p3) + t1*(v1+v3)
    c2 = (p2+p3) + t2*(v2+v3)
    v = (c2-c1) / (t2 - t1)
    p = c1 - t1 * v
    print(f"{p=}; {v=}")
    return sum(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))


