#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection, RelativeDirection
from collections import defaultdict

class Grid:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def at(self, p):
        if p.x < 0 or p.y < 0 or p.x >= self.width or p.y >= self.height:
            return None
        return self.data[p.y][p.x]

    def neighbors(self, p):
        points = [p.move(direction) for direction in CardinalDirection]
        return [p for p in points if p.x >= 0 and p.y >= 0 and p.x < self.width and p.y < self.height]

class Region:
    def __init__(self, positions, type):
        self.positions = positions
        self.type = type

    def merge(self, other):
        if self is other:
            return self
        return Region(self, self.positions.union(other.positions))

    def area(self):
        return len(self.positions)

    def perimiter(self):
        return sum([sum([p.move(d) not in self.positions for d in CardinalDirection]) for p in self.positions])

    def edges(self):
        visited = set()
        edges = 0
        dbg.print(f"Finding edges of {self.type}")
        dbg.print(f"{self.positions=}")
        for p in self.positions:
            if p in visited:
                continue
            out = CardinalDirection.NORTH
            if p.move(out) not in self.positions:
                # Found a top edge
                start = p
                dbg.print(f"Found a top edge at {p}")
                along_edge = CardinalDirection.EAST
                back = along_edge.turn(RelativeDirection.BACKWARDS)
                # Slide back to the start of the found edge before starting
                while True:
                    next = p.move(back)
                    if next in self.positions and next.move(out) not in self.positions:
                        p = next
                    else:
                        break
                if start != p:
                    dbg.print(f"Slid back to {p}")
                start = p
                first = True
                while first or p != start or out != CardinalDirection.NORTH:
                    first = False
                    if out == CardinalDirection.NORTH:
                        visited.add(p)
                    p_out = p.move(out)
                    p_along = p.move(along_edge)
                    if p_out in self.positions:
                        # Inside corner
                        dbg.print(f"inside corner at {p} facing {out}")
                        out = out.turn(RelativeDirection.LEFT)
                        along_edge = along_edge.turn(RelativeDirection.LEFT)
                        p = p_out
                        edges += 1
                    elif p_along not in self.positions:
                        # Outside corner
                        dbg.print(f"outside corner at {p} facting {along_edge}")
                        out = out.turn(RelativeDirection.RIGHT)
                        along_edge = along_edge.turn(RelativeDirection.RIGHT)
                        edges += 1
                    else:
                        # Just moving along an edge
                        p = p_along
        dbg.print(f"Found {edges} edges")
        return edges

    def price(self):
        return self.area() * self.perimiter()

    def bulk_price(self):
        return self.area() * self.edges()

    def __repr__(self):
        return f"Region of {self.area()} {self.type}'s with perimiter {self.perimiter()} and {self.edges()} edges"

    @classmethod
    def from_file(cls, file):
        grid = Grid([[c for c in line.strip()] for line in file])
        visited = set()
        regions = []
        for y in range(grid.height):
            for x in range(grid.width):
                p = Point(x,y)
                if p in visited:
                    continue
                type = grid.at(p)
                fringe = set()
                region_points = set()
                fringe.add(p)
                while len(fringe) > 0:
                    p = fringe.pop()
                    region_points.add(p)
                    for p2 in grid.neighbors(p):
                        if grid.at(p2) == type and p2 not in fringe and p2 not in region_points:
                            fringe.add(p2)
                visited = visited.union(region_points)
                regions.append(cls(region_points, type))
        return regions


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        regions = Region.from_file(file)

    if not part2:
        return sum(region.price() for region in regions)
    prices = [region.bulk_price() for region in regions]
    dbg.print(prices)
    return sum(prices)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

