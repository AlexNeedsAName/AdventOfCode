#!/usr/bin/env python3
import argparse
from aoc_util import dbg
from collections import defaultdict


def is_valid(update, rules):
    for i,number in enumerate(update):
        # The rule list contains all numbers that must be after the current number
        # So if they appear earlier in the list, they break the rule
        for rule in rules[number]:
            if rule in update[:i]:
                dbg.print(f"Update {update} breaks rule {number}|{rule}")
                return False
    return True

# Does a selection/insertion sort on any elements that violate the rules
# Select the first element that violates a rule, then insert it earlier to make sure it isn't a problem
# Back up to verify that element doesn't have anything later in the list that needs to go before it and repeat
def fix_order(update, rules):
    i = 0
    while i < len(update):
        number = update[i]
        for rule in rules[number]:
            if rule in update[:i]:
                update.pop(update.index(rule))
                update.insert(i, rule)
                i -= 2
                break
        i += 1
    return True

def middle(list):
    return list[len(list)//2]

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        rules = defaultdict(list)
        rules = defaultdict(list)
        for line in file:
            line = line.strip()
            if len(line) == 0:
                break
            a, b = (int(token) for token in line.split('|'))
            rules[a].append(b)

        updates = []
        for line in file:
            line = line.strip()
            updates.append([int(token) for token in line.split(',')])

        if not part2:
            total = 0
            for update in updates:
                if is_valid(update, rules):
                    mid =  middle(update)
                    total += mid
                    dbg.print(mid)
            return total

        total = 0
        for update in updates:
            if not is_valid(update, rules):
                before = [i for i in update]
                fix_order(update, rules)
                assert is_valid(update, rules)
                dbg.print(f"{before} -> {update}")
                mid = middle(update)
                total += mid
                dbg.print(mid)
        return total



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

