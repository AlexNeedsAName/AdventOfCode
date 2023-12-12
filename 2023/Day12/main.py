#!/usr/bin/env python3
import argparse
from enum import Enum
import itertools

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class Condition(Enum):
    WORKING = '.'
    BROKEN = '#'
    UNKNOWN = '?'

class Conditions:
    def __init__(self, conditions, groups):
        self.conditions = conditions
        self.groups = groups

    def is_valid(self):
        if Condition.UNKNOWN in self.conditions:
            raise ValueError("Must not contain any unknowns")

        groups = []
        group_size = 0
        for condition in self.conditions:
            dbg_print(condition, level=3)
            if condition == Condition.BROKEN:
                group_size += 1
                dbg_print(f'Increasing group_size to {group_size}', level=3)
            elif condition == Condition.WORKING and group_size > 0:
                groups.append(group_size)
                dbg_print(f'Pushing back group of size {group_size}', level=3)
                group_size = 0
        if group_size > 0:
            groups.append(group_size)
            dbg_print(f'Pushing back final group of size {group_size}', level=3)

        if len(groups) != len(self.groups):
            return False
        for a,b in zip(groups, self.groups):
            if a != b:
                return False
        return True

    def possibilities(self):
        dbg_print(self)
        indicies = []
        for i,condition in enumerate(self.conditions):
            if condition == Condition.UNKNOWN:
                indicies.append(i)
        num_unknowns = len(indicies)

        broken_total = sum(self.groups)
        missing_brokens = broken_total - self.conditions.count(Condition.BROKEN)

        results = []
        for values in itertools.product((Condition.WORKING, Condition.BROKEN), repeat=num_unknowns):
            if values.count(Condition.BROKEN) != missing_brokens:
                continue
            conditions = self.conditions.copy()
            for i,value in enumerate(values):
                conditions[indicies[i]] = value
            result = Conditions(conditions, self.groups)
            if result.is_valid():
                dbg_print(result, result.is_valid())
                results.append(result)

        return results

#    def possibilities(self):
#        return []



    @classmethod
    def from_file(cls, file):
        return cls.from_line(file.readline())

    @classmethod
    def from_line(cls, line, fold_count=1):
        conditions, groups = line.strip().split()
        conditions = [Condition(c) for c in conditions]
        groups = [int(v) for v in groups.split(',')]

        c = conditions.copy()
        c.insert(0, Condition.UNKNOWN)
        g = groups.copy()
        for i in range(fold_count-1):
            conditions.extend(c)
            groups.extend(g)

        return cls(conditions, groups)

    def __str__(self):
#        return ' '.join([''.join(condition.value for condition in self.conditions), ','.join(str(group) for group in self.groups)])
        return ''.join(condition.value for condition in self.conditions)

    def __repr__(self):
        return f'Conditions({self.conditions}, {self.groups})'

def part1(input_file):
    total = 0
    with open(input_file, 'r') as file:
        for line in file:
            c = Conditions.from_line(line)
            p = c.possibilities()
            print(len(p), tuple(str(a) for a in p))
            total += len(p)
    return total

def part2(input_file):
    total = 0
    with open(input_file, 'r') as file:
        for line in file:
            c = Conditions.from_line(line, fold_count=5)
            total += len(c.possibilities())
    return total



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))
#    print(part2(args.filename))

