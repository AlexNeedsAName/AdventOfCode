#!/usr/bin/env python3
import functools
import argparse
from progressbar import progressbar

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print('  ' * (level-1), *args, **kwargs)


found_in_map = 0
not_found = 0

class Range:
    def __init__(self, range=None):
        if range is None:
            self.min = float('inf')
            self.max = -self.min
        else:
            self.min, self.max = range

    def extend(self, other):
        try:
            return Range((min(self.min, other.min), max(self.max, other.max)))
        except Exception as e:
            print(f"Can't extend range {self} with {other}")
            raise e

    def raise_max(self, new_max):
        return Range((self.min, max(self.max, new_max)))

    def reduce_min(self, new_min):
        return Range((min(self.min, new_min), self.max))

    def __repr__(self):
        return f'Range(({self.min}, {self.max}))'

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.min, self.max))

class MapRange:
    def __init__(self, dst_range_start, src_range_start, range_length):
        self.dst_start = dst_range_start
        self.src_start = src_range_start
        self.range_length = range_length

    @classmethod
    def from_string(cls, string):
        return cls(*(int(token) for token in string.split(' ')))


    def get_range(self, src_range):
#        min_src = max(src_range.min, self.src_start)
#        max_src = min(src_range.max, self.src_start + self.range_length)
        return Range((self.get(src_range.min), self.get(src_range.max)+1))

#        values = [self.get(max(src_range.min), self.get(src_range.max)]
#        min_into = src_range.min - self.src_start
#        max_into = src_range.max - self.src_start
#        if min_into < 0:
#            values.append(self.get(self.src_start))
#        if max_into >= self.range_length:
#            values.append(self.get(self.src_start + self.range_length))
#        return Range((min(values), max(values)))


    def get(self, src):
        into_range = src - self.src_start
        if into_range >= self.range_length or into_range < 0:
            global not_found
            not_found += 1
            #print(f'Source {src} does not belong to range {self}, returning {src}')
            return src
#            raise ValueError(f'Source {src} does not belong to range {self}')
        return self.dst_start + into_range

    def __repr__(self):
#        return f'MapRange({self.dst_start}, {self.src_start}, {self.range_length})'
        return f'MapRange({self.src_start}, {self.src_start + self.range_length})'


class Map:
    def __init__(self, name_line, file):
        ranges = []
        self.name = name_line.strip().split(':')[0]
        print(self.name)
        self.src_type, _, self.dst_type = self.name.split(' ')[0].split('-')

        for line in file:
            line = line.strip()
            if len(line) == 0:
                break
            range = MapRange.from_string(line)
            ranges.append((range.src_start, range))
        ranges.sort()
        self.ranges = ranges[::-1]
        #print(ranges)

    def get_ranges(self, src_ranges):
        dbg_print(f'getting {src_ranges} from {self.name}', level=2)

        first_range =  self.ranges[0][1]
        last_range =  self.ranges[-1][1]

        result_ranges = set()

        for src_range in src_ranges:
            if src_range.max > first_range.src_start + first_range.range_length:
                range_min = max(src_range.min, first_range.src_start + first_range.range_length)
                result_ranges.add(Range((range_min, src_range.max)))

            for range_start, range in self.ranges:
                dbg_print(f'Checking {src_range} against {range}', level=3)
                if src_range.min > range_start + range.range_length:
                    break
                check_min = max(range_start, src_range.min)
                check_max = min(range_start + range.range_length-1, src_range.max-1)
#                dbg_print(f'{check_min}-{check_max}', level=3)
                if check_min <= check_max:
                    dbg_print(f'  {check_min}-{check_max}', level=3)
                    dbg_print(f'  ranges overlap', level=3)
                    new_range = (range.get_range(Range((check_min, check_max))))
                    result_ranges.add(new_range)
                    dbg_print(f'  {new_range}', level=3)

            if src_range.min < last_range.src_start:
                range_max = min(src_range.max-1, last_range.src_start)
                result_ranges.add(Range((src_range.min, range_max)))


        return result_ranges
#                else:
#                    dbg_print(f'min is greater than max, not using range', level=3)

# Range overlap possibilities:
# 1. No overlap. src.max < range.min
# src:    (       )
# rng:              (        )
# 2. overlap at end. src.max >= range.min
# src:    (       )
# rng:         (        )
# 3. subset. src.max >= range.min, but also src.max <= range.max
# src:    (       )
# dst:  (           )



    def get(self, src):
        #print(f'getting {src} from {self.name}')
        for range_start, range in self.ranges:
            if range_start > src:
                continue
            global found_in_map
            found_in_map += 1
            return range.get(src)
        global not_found
        not_found += 1
        return src


def part1(input_file):
    maps = {}
    with open(input_file, 'r') as file:
        seeds = [int(token) for token in file.readline().split(':')[-1].strip().split(' ')]
        #print(f'seeds: {seeds}')
        assert len(file.readline().strip()) == 0
        line = file.readline()
        while line:
            map = Map(line, file)
            maps[map.src_type] = map
            line = file.readline()

        locations = []
        for seed in seeds:
            type = 'seed'
            value = seed
            while type != 'location':
                map = maps[type]
                #print(f'translating from {type} {value} to {map.dst_type}')
                value = map.get(value)
                type = map.dst_type
                #print(f'result is {type} {value}')
            #print(f'seed {seed} goes in location {value}')
            locations.append(value)
        return min(locations)


def part2(input_file):
    maps = {}
    with open(input_file, 'r') as file:
        seed_pairs = [int(token) for token in file.readline().split(':')[-1].strip().split(' ')]

        seed_ranges = []
        for i in range(0,len(seed_pairs),2):
            seed_ranges.append(Range((seed_pairs[i], seed_pairs[i]+seed_pairs[i+1])))
        #print(f'seeds: {seeds}')
        assert len(file.readline().strip()) == 0
        line = file.readline()
        while line:
            map = Map(line, file)
            maps[map.src_type] = map
            line = file.readline()

#        return maps

        type = 'seed'
        values = seed_ranges
        while type != 'location':
            map = maps[type]
            print(f'translating {len(values)} ranges from {type} to {map.dst_type}')
            values = map.get_ranges(values)
            type = map.dst_type
            #print(f'result is {type} {value}')
        #print(f'seed {seed} goes in location {value}')

        print(values)

        min_loc = float('inf')
        for rslt_range in values:
            if rslt_range.min < min_loc:
                min_loc = rslt_range.min

        return min_loc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

#    print(part1(args.filename))
    print(part2(args.filename))

