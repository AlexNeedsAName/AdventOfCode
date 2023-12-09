#!/usr/bin/env python3
import argparse
import itertools
from time import sleep
from math import lcm
from progressbar import progressbar

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


nodes = {}

class Node:
    def __init__(self, id, left, right):
        self.id = id
        self.left = left
        self.right = right
        nodes[id] = self

    def get_left(self):
        return nodes[self.left]

    def get_right(self):
        return nodes[self.right]

    def __repr__(self):
        return f'{self.id} = ({self.left}, {self.right})'

    @classmethod
    def from_string(cls, line):
        id, _, left, right = line.strip().replace('(', '').replace(')', '').replace(',', '').split()
        return cls(id, left, right)

def part1(input_file):
    with open(input_file, 'r') as file:
        instructions = [char for char in file.readline().strip()]
        file.readline()
        for line in file:
            Node.from_string(line)

    count = 0
    node = nodes['AAA']
    for instruction in itertools.cycle(instructions):
        last_id = node.id
        if instruction == 'L':
            node = node.get_left()
        elif instruction == 'R':
            node = node.get_right()
        else:
            print(f'unknown direction {instruction}')
        count += 1

        dbg_print(f'{last_id}.{instruction} -> {node.id}')

        if node.id == 'ZZZ':
            break

    return count


def part2(input_file):
    with open(input_file, 'r') as file:
        instructions = [char for char in file.readline().strip()]
        file.readline()
        start_set = set()
        end_set = set()
        for line in file:
            node = Node.from_string(line)
            if node.id[-1] == 'A':
                start_set.add(node)
            elif node.id[-1] == 'Z':
                end_set.add(node)

    count = 0
    current = start_set
    for instruction in itertools.cycle(instructions):
        new_set = set()
        done = True
        for node in current:
            last = node
            if instruction == 'L':
                node = node.get_left()
            elif instruction == 'R':
                node = node.get_right()
            else:
                print(f'unknown direction {instruction}')

            dbg_print(f'{last}.{instruction} -> {node}')

            new_set.add(node)

            if node not in end_set:
                done = False
        count += 1
        current = new_set
        dbg_print('\n')
        if done:
            break

    return count


def part2attempt2(input_file):
    with open(input_file, 'r') as file:
        instructions = [char for char in file.readline().strip()]
        file.readline()
        start_set = set()
        end_set = set()
        for line in file:
            node = Node.from_string(line)
            if node.id[-1] == 'A':
                start_set.add(node)
            elif node.id[-1] == 'Z':
                end_set.add(node)

    total = 1
    lead_ups = []
    cycle_lengths = []
    end_states = []
    for j,start_node in enumerate(start_set):
        potential_ends = []
        node = start_node
        count = 0
        seen = {}
        for i,instruction in itertools.cycle(enumerate(instructions)):
            last = node
            if instruction == 'L':
                node = node.get_left()
            elif instruction == 'R':
                node = node.get_right()
            else:
                print(f'unknown direction {instruction}')

            dbg_print(f'{last}.{instruction} -> {node} ({i})', level=2)
            count += 1

            #print(node, i)

            if node in end_set:
                potential_end = count

            state = (node, i)

            if state in seen.keys():
                last_saw = seen[state]
                dbg_print(f'cycle {j} repeats after {count}. last saw this state at {last_saw}')
                lead_ups.append(last_saw)
                cycle_lengths.append(count - last_saw)
                end_states.append(potential_end)
                break
            seen[state] = count



    loop_length = lcm(*cycle_lengths)

    # I still don't believe this would work on arbitrary inputs.
    return loop_length

    print(f"Cycles loop after {loop_length} of the shortest cycle")
    for _ in progressbar(range(loop_length * len(cycle_lengths))):
        for i,end in enumerate(end_states):
            closest_end = min(end_states)
            if end == closest_end:
                cycle_length = cycle_lengths[i]
                end_states[i] += cycle_length


        if min(end_states) == max(end_states):
            break

    return end_states[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))
    print(part2attempt2(args.filename))


