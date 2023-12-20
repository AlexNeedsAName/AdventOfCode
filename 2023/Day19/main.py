#!/usr/bin/env python3
import argparse
from enum import Enum
from aoc_util import dbg, InclusiveRange
from math import prod

categories = ('x', 'm', 'a', 's')

class Part(dict):
    @classmethod
    def from_string(cls, string):
        result = Part()
        for assignment in string.strip()[1:-1].split(','):
            key, value = assignment.split('=')
            result[key]=int(value)
        return result

    def rating(self):
        return sum(self.values())

    def count(self):
        return prod(range.count() for range in self.values())

    def __getitem__(self, key):
        if key not in categories:
            raise KeyError(f"Invalid key {key}")
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if key not in categories:
            raise KeyError
        return dict.__setitem__(self, key, value)

    def __str__(self):
        value_str = ', '.join(f'{key}={self[key]}' for key in categories)
        return f'{{{value_str}}}'

class Rule:
    def __init__(self, dest, key='x', value=0, op='>'):
        self.value = value
        self.op = op
        self.dest = dest
        self.key = key

    def applies_to(self, part):
        if self.op == '>':
            return part[self.key] > self.value
        elif self.op == '<':
            return part[self.key] < self.value
        return False

    def split_range(self, part):
        range = part[self.key]
        approved = Part(part.copy())
        rejected = Part(part.copy())
        if self.op == '>':
            approved[self.key] = range.intersection(InclusiveRange(self.value+1, float('inf')))
            rejected[self.key] = range.intersection(InclusiveRange(-float('inf'), self.value))
        elif self.op == '<':
            approved[self.key] = range.intersection(InclusiveRange(-float('inf'), self.value-1))
            rejected[self.key] = range.intersection(InclusiveRange(self.value, float('inf')))
        return approved, rejected

    @classmethod
    def from_string(self, string):
        try:
            rule_str, dest = string.split(':')
            category = rule_str[0]
            operation = rule_str[1]
            value = int(rule_str[2:])
            return Rule(dest,category,value,operation)
        except ValueError:
            return Rule(string)

    def __str__(self):
        return f'{self.key} {self.op} {self.value}, {self.dest}'

    def __repr__(self):
        return str(self)


class Workflow:
    workflows = {'A': True, 'R': False}
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules
        Workflow.workflows[self.name] = self
        #print(f'Workflow.workflows = {Workflow.workflows}')

    def evaluate(self, part):
        workflow = self
        while isinstance(workflow, Workflow):
            for rule in workflow.rules:
                if rule.applies_to(part):
                    workflow = Workflow.workflows[rule.dest]
                    break
        return workflow

    def evaluate_ranges(self, part, depth=0):
        dbg.print(f'{"  " * depth}evaluating part {part} with workflow {self.name}')
        total_accepted = 0
        total_rejected = 0
        remaining = part
        for rule in self.rules:
            dbg.print(f'{"  " * depth}checking rule {rule} on remaining part {remaining}')
            approved,remaining = rule.split_range(remaining)
            next = Workflow.workflows[rule.dest]
            try:
                accepted_count, rejected_count = Workflow.workflows[rule.dest].evaluate_ranges(approved, depth=depth+1)
            except AttributeError:
                if next:
                    accepted_count = approved.count()
                    rejected_count = 0
                else:
                    accepted_count = 0
                    rejected_count = approved.count()
                dbg.print(f'{"  " * (depth+1)}Reached terminal state with part {approved}. Accepted {accepted_count} and rejected {rejected_count}')
            total_accepted += accepted_count
            total_rejected += rejected_count

        if total_accepted + total_rejected != part.count():
            print(f"{'  ' * depth}total accepted: {total_accepted}")
            print(f"{'  ' * depth}rejected: {total_rejected}")
            print(f"{'  ' * depth}total: {part.count()}")
#            raise AssertionError
        return total_accepted, total_rejected

    @classmethod
    def from_string(cls, string):
        name, string = string.strip().split('{')
        rules = string[:-1].split(',')
        rules = tuple(Rule.from_string(rule) for rule in rules)
        result = cls(name, rules)
        dbg.print(result)
        return result

    def __str__(self):
        result = ', '.join(str(rule) for rule in self.rules)
        return f'{self.name} {{{result}}}'

    def __repr__(self):
        return str(self)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        for line in file:
            if len(line.strip()) == 0:
                break
            Workflow.from_string(line)

        #print(Workflow.workflows)

        start = Workflow.workflows['in']
        if not part2:
            total = 0
            for line in file:
                p = Part.from_string(line)
                accepted = start.evaluate(p)
                if accepted:
                    rating = p.rating()
                    dbg.print(f'Part {p} is accepted (rating {rating})')
                    total += rating
                else:
                    dbg.print(f'Part {p} is rejected')
            return total
        else:
            p = Part()
            r = InclusiveRange(1,4000)
            for c in categories:
                p[c] = r

            accepted, rejected = start.evaluate_ranges(p)

#            assert accepted + rejected == 4000**4

            return accepted



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))

