#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection
import astar
import itertools
from collections import defaultdict

class RaceState:
    def __init__(self, position, cheats_left, cheat_time_left):
        self.position = position
        self.cheats_left = cheats_left
        self.cheat_time_left = min(cheat_time_left, 0)

    def __hash__(self):
        return hash((self.position, self.cheats_left, self.cheat_time_left))

    def __eq__(self, other):
        return self.position == other.position and self.cheats_left == other.cheats_left and self.cheat_time_left == other.cheat_time_left


class RaceState2:
    def __init__(self, position, cheat_index):
        self.position = position
        self.cheat_index = cheat_index

    def __hash__(self):
        return hash((self.position, self.cheat_index))

    def __eq__(self, other):
        return self.position == other.position and self.cheat_index == other.cheat_index


class Maze(astar.AStar):
    def __init__(self, walls, start, end, width, height):
        self.walls = set(walls)
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.cheat_duration = 2
        self.cheat_tiles = []


    def find_cheats(self, save_at_least=1):
#        self.cheat_tiles = [Point(6, 7), Point(5,7)]
        self.cheat_tiles = []
        path = self.astar(RaceState2(self.start, 0), self.end)
        positions = [node.position for node in path]
        base_cost = len(positions)-1
        print("Base path:")
        print(self.draw(positions))
        print(f"This path costs {base_cost}")

        counts = defaultdict(lambda: 0)
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x,y)
                if p not in self.walls:
                    continue
                for cheat_paths in itertools.product(CardinalDirection, repeat=self.cheat_duration-1):
                    self.cheat_tiles = [p]
                    for direction in cheat_paths:
                        self.cheat_tiles.append(self.cheat_tiles[-1].move(direction))
                    if self.cheat_tiles[-1] in self.walls:
                        continue
#                    print(f"Solving with cheat tiles {self.cheat_tiles}")
                    path = self.astar(RaceState2(self.start, 0), self.end)
                    if path is None:
#                        print("No solution")
                        continue
                    positions = [node.position for node in path]
                    cheat_cost = len(positions)-1
                    savings = base_cost - cheat_cost
                    if savings >= save_at_least:
                        counts[savings] += 1
                        print(self.draw(positions))
                        print(f"This path costs {cheat_cost} and saves {savings}")
#                    else:
#                        print(f"Savings are just {savings}")

        for savings,count in counts.items():
            print(f"There are {count} cheats that save {savings} picoseconds")

        return sum(counts.values())


    def neighbors(self, node):
        result = []
        for direction in CardinalDirection:
            next = node.position.move(direction)
            if next.x < 0 or next.y < 0 or next.x >= self.width or next.y >= self.height:
                continue
            if node.cheat_index is not None and node.cheat_index < len(self.cheat_tiles):
                if next == self.cheat_tiles[node.cheat_index]:
                    result.append(RaceState2(next, node.cheat_index+1))
                if node.cheat_index > 0:
                    # If we've started the cheat, we must finish it. Can't just stop part way through
                    # To do that, we skip the regular wall check
                    continue
            if next not in self.walls:
                result.append(RaceState2(next, 0 if node.cheat_index == 0 else None))

#            if next in self.walls and node.cheat_time_left <= 0:
#                if node.cheats_left > 0:
#                    result.append(RaceState(next, node.cheats_left-1, self.cheat_duration-1))
#                continue
#            result.append(RaceState(next, node.cheats_left, node.cheat_time_left-1))
        return result

    def distance_between(self, p1, p2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        x1,y1 = current.position
        x2,y2 = goal
        return abs(x1-x2)+abs(y1-y2)

    def is_goal_reached(self, current, goal):
        return current.position == goal


    def draw(self, positions):
        positions = set(positions)
        result = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = Point(x,y)
                if p in self.cheat_tiles:
                    line.append(str(self.cheat_tiles.index(p)+1))
                elif p == self.start:
                    line.append('S')
                elif p == self.end:
                    line.append('E')
                elif p in positions and p in self.walls:
                    line.append('*')
                elif p in positions:
                    line.append('O')
                elif p in self.walls:
                    line.append('#')
                else:
                    line.append('.')
            result.append(''.join(line))
        return '\n'.join(result)



    @classmethod
    def from_file(cls, file):
        width = -1
        height = -1
        walls = set()
        start = None
        end = None
        for y,line in enumerate(file):
            height = y
            for x,c in enumerate(line):
                width = x
                if c == '#':
                    walls.add(Point(x,y))
                elif c == 'S':
                    start = Point(x,y)
                elif c == 'E':
                    end = Point(x,y)
        x += 1
        y += 1

        return Maze(walls, start, end, width, height)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        maze = Maze.from_file(file)

#    path = list(maze.astar(RaceState(maze.start, 0, 0), maze.end))
#    base_cost = len(path)
#
#    paths = list(maze.astar(RaceState(maze.start, 0, 0), maze.end), findTop=100)
#    for path in paths:
#        positions = set(node.position for node in path)
#        print(maze.draw(positions))

    return maze.find_cheats(1 if input_file == "small.txt" else 100)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
#    print(problem(args.filename, part2=True))

