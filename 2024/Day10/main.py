#!/usr/bin/env python3
import argparse
import search
from aoc_util import dbg, CardinalDirection, Point


class TrailSearch(search.SearchProblem):
    def __init__(self, start_state):
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state.isWinState()

    def getSuccessors(self, state):
        return state.generateSucessors()

    def getCostOfActions(self, actions):
        return len(actions)


def try_int(value, fallback):
    try:
        return int(value)
    except ValueError:
        return fallback


class TrailMap:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)

        self.starts = []
        self.ends = []
        for y,line in enumerate(grid):
            for x,height in enumerate(line):
                if height == 0:
                    self.starts.append(Point(x,y))
                elif height == 9:
                    self.ends.append(Point(x,y))

        print(f"Starts are {self.starts}")
        print(f"Ends are {self.ends}")


    @classmethod
    def from_file(cls, file):
        grid = []
        for line in file:
            grid.append([try_int(c,-1) for c in line.strip()])
        return cls(grid)


    def at(self, point):
        if point.x < 0 or point.y < 0 or point.x >= self.width or point.y >= self.width:
            return None
        return self.grid[point.y][point.x]


    def find_all_ends_from(self, start):
        solutions = []
        for end in self.ends:
            start_state = TrailSearchState(self, start, end, set())
            problem = TrailSearch(start_state)
            result = search.dfs(problem)
            if result is not None:
                solutions.append(result)
        return solutions

    def find_score(self):
        scores = []
        for start in self.starts:
            result = self.find_all_ends_from(start)
            scores.append(len(result))
        print(scores)
        return sum(scores)

    def find_all_trails_from(self, start):
        solutions = []
        for end in self.ends:
            start_state = TrailSearchState(self, start, end, set())
            problem = TrailSearch(start_state)
            result = search.astar(problem, find_all=True)
            if result is not None:
                solutions.extend(result)
        return solutions

    def find_rating(self):
        ratings = []
        for start in self.starts:
            trails = self.find_all_trails_from(start)
            ratings.append(len(trails))
        print(ratings)
        return sum(ratings)

    def mark_trail(self, positions):
        return '\n'.join(''.join(str(num) if Point(x,y) in positions else '.' for x,num in enumerate(line)) for y,line in enumerate(self.grid))

    def __str__(self):
        return '\n'.join(''.join(str(num) if num >= 0 else '.' for num in line) for line in self.grid)


class TrailSearchState:
    def __init__(self, map, position, target, visited, dir=None):
        self.map = map
        self.position = position
        self.target = target
        self.visited = frozenset(list(visited) + [self.position])
        #print(f"Moved {dir}")
        #print(f"{position=}; {visited=}")
        #print(self.map.mark_trail(self.visited))

    def isWinState(self):
        return self.position == self.target

    def generateSucessors(self):
        sucessors = []
        height = self.map.at(self.position)
        for direction in CardinalDirection:
            new_position = self.position.move(direction)
            if new_position in self.visited:
                continue
            new_height = self.map.at(new_position)
            if new_height is None:
                continue
            if new_height - height != 1:
                continue
            sucessors.append((self.__class__(self.map, new_position, self.target, self.visited, direction), direction, 1))
        return sucessors

    def __hash__(self):
        return hash(f'{hash(self.visited)} {self.position}')



def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        map = TrailMap.from_file(file)

    print(map,'\n')
    if not part2:
        score = map.find_score()
    else:
        score = map.find_rating()

    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

