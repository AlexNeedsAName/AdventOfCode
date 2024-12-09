#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point
from collections import defaultdict

class AntennaMap:
    def __init__(self, locations_by_type, sorted_nonempty_tiles, width, height):
        self.locations_by_type = locations_by_type
        self.sorted_nonempty_tiles = sorted_nonempty_tiles
        self.antinodes = []
        self.width = width
        self.height = height


    @classmethod
    def from_file(cls, file):
        locations_by_type = defaultdict(list)
        sorted_nonempty_tiles = []
        height = 0
        width = 0
        for y,line in enumerate(file):
            height = y
            for x,char in enumerate(line.strip()):
                width = x
                if char == '.' or char == '#':
                    continue
                loc = Point(x,y)
                locations_by_type[char].append(loc)
                sorted_nonempty_tiles.append((loc, char))
        return cls(locations_by_type, sorted_nonempty_tiles, width+1, height+1)


    def get_antinode_locations(self):
        return set(loc for loc,c in self.antinodes)


    def mark_antinodes(self, resonant=False):
        for type in self.locations_by_type.keys():
            locations = self.locations_by_type[type]
            for i,(ax,ay) in enumerate(locations):
                for bx,by in locations[i+1:]:
                    rise = by-ay
                    run = bx-ax
                    if not resonant:
                        new_nodes = [((Point(ax-run,ay-rise), type)), ((Point(bx+run,by+rise), type))]
                        new_nodes = [node for node in new_nodes if node[0].x >= 0 and node[0].x < self.width and node[0].y >= 0 and node[0].y < self.height]
                    else:
                        new_nodes = []
                        nx,ny = ax,ay
                        while nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
                            new_nodes.append(((nx,ny), type))
                            nx -= run
                            ny -= rise
                        nx,ny = bx,by
                        while nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
                            new_nodes.append(((nx,ny), type))
                            nx += run
                            ny += rise
                    self.antinodes.extend(new_nodes)


    def __str__(self):
        result = [ ['.'] * self.width for j in range(self.height) ]
        for (x,y),c in self.antinodes:
            result[y][x] = '#'
        for (x,y),c in self.sorted_nonempty_tiles:
            result[y][x] = c
        return '\n'.join(''.join(line) for line in result)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        map = AntennaMap.from_file(file)
    print(map,'\n')
    map.mark_antinodes(resonant=part2)
    print(map)
    return len(map.get_antinode_locations())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

