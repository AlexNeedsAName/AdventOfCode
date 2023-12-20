#!/usr/bin/env python3
import argparse
from enum import Enum
from aoc_util import dbg

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

    def __getitem__(self, key):
        if key not in categories:
            raise KeyError
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if key not in categories:
            raise KeyError
        return dict.__setitem__(self, key, value)

    def __str__(self):
        value_str = ','.join(f'{key}={self[key]}' for key in categories)
        return f'{{{value_str}}}'

class Rule:
    def __init__(self, dest, rule=lambda part: True, str=None):
        self.rule = rule
        self.dest = dest
        self.str = str

    def applies_to(self, part):
        return self.rule(part)

    @classmethod
    def from_string(self, string):
        try:
            rule_str, dest = string.split(':')
            category = rule_str[0]
            operation = rule_str[1]
            value = int(rule_str[2:])
            if operation == '<':
                rule = lambda part: part[category] < value
            elif operation == '>':
                rule = lambda part: part[category] > value
            else:
                raise ArgumentError(f"Invalid operation '{operation}'")
            return Rule(dest,rule,str=f'{category} {operation} {value}')
        except ValueError:
            return Rule(string,str=string)

    def __str__(self):
        return self.str

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
#    print(problem(args.filename, part2=True))

