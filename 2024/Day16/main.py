#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection, RelativeDirection
#import search
import astar
import sys
from collections import defaultdict


class SearchNode:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


    def __hash__(self):
        return hash((self.position, self.direction))


    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction


class Maze(astar.AStar):
    def __init__(self, width, height, walls, start, end):
        self.walls = walls
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.nodes = set()


    def is_corner(self, position):
        adj_positions = [position.move(direction) for direction in CardinalDirection]
        if list(adj_position in self.walls for adj_position in adj_positions).count(True) != 2:
            return False
        is_straight = (adj_positions[0] not in self.walls and adj_positions[2] not in self.walls) or (adj_positions[1] not in self.walls and adj_positions[3] not in self.walls)
        return not is_straight


    def neighbors(self, node):
        neighbors = [SearchNode(node.position, node.direction.turn(direction)) for direction in (RelativeDirection.LEFT, RelativeDirection.RIGHT)]
        next = node.position.move(node.direction)
        if next not in self.walls:
            neighbors.append(SearchNode(next, node.direction))
        return neighbors

    def distance_between(self, n1, n2):
        # n1 and n2 must be adjacent
        if n1.position == n2.position:
            # If the position is the same it must be a turn
            return 1000
        else:
            # If the position is not the same it must be a single step
            return 1

    def heuristic_cost_estimate(self, current, goal):
        return 0
        x1,y1 = current.position
        x2,y2 = goal
        return abs(x1-x2)+abs(y1-y2)

    def is_goal_reached(self, current, goal):
        return current.position == goal


    @classmethod
    def from_file(cls, file):
        walls = set()
        width = 0
        height = 0
        start = Point(-1,-1)
        end = Point(-1,-1)
        for y,line in enumerate(file):
            height = y
            for x,c in enumerate(line.strip()):
                width = x
                if c == "#":
                    walls.add(Point(x,y))
                elif c == "S":
                    start = Point(x,y)
                elif c == "E":
                    end = Point(x,y)
        width += 1
        height += 1
        return cls(width, height, walls, start, end)


    def draw(self, path=None):
        if path is None:
            path = []
        steps = {node.position: node.direction for node in path}

        result = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = Point(x,y)
                if p == self.start:
                    line.append('S')
                elif p == self.end:
                    line.append('E')
                elif p in self.nodes:
                    line.append('O')
                elif p in steps.keys():
                    line.append(steps[p].as_char())
                elif p in self.walls:
                    line.append('#')
                else:
                    line.append('.')
            result.append(''.join(line))
        return '\n'.join(result)


    def __str__(self):
        return self.draw()


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        maze = Maze.from_file(file)

    print(maze)
    if not part2:
        path = list(maze.astar(SearchNode(maze.start, CardinalDirection.EAST), maze.end))
        print(maze.draw(path))
        return sum(maze.distance_between(a,b) for a,b in zip(path, path[1:]))
    paths = maze.astar(SearchNode(maze.start, CardinalDirection.EAST), maze.end, findAll=True)
    print(f"Found {len(paths)} paths")
    used = set()
    for path in paths:
        for node in path:
            used.add(node.position)
    return len(used)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

