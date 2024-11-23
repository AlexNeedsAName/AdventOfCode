#!/usr/bin/env python3
import sys

bag = {'red': 12, 'green': 13, 'blue': 14}

def possible_state(bag, shown):
    for color in bag.keys():
        if bag[color] < shown[color]:
            print(f'color {color} {shown[color]} > {bag[color]}')
            return False
            print(f'color {color} {shown[color]} <= {bag[color]}')
    return True

def min_possible(prior_best, shown):
    for color in prior_best.keys():
        if prior_best[color] < shown[color]:
            prior_best[color] = shown[color]
    return prior_best

def power(bag):
    return bag['red'] * bag['green'] * bag['blue']

def part1(input_file):
    total = 0
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            game, states = line.split(':')
            game = int(game.split(' ')[-1])
            replacements = states.split(";")
            print(game, replacements)
            possible = True
            for replacement in replacements:
                shown = {}
                for color in bag.keys():
                    shown[color] = 0
                shown_balls = replacement.split(',')
                for token in shown_balls:
                    count, color = token.split()
                    count = int(count)
                    shown[color] = count
                possible = possible and possible_state(bag, shown)
            if possible:
                total += game
    return total

def part2(input_file):
    total = 0
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            game, states = line.split(':')
            game = int(game.split(' ')[-1])
            replacements = states.split(";")
            print(game, replacements)
            best_bag = {'red': 0, 'green': 0, 'blue': 0 }
            for replacement in replacements:
                shown = {}
                for color in bag.keys():
                    shown[color] = 0
                shown_balls = replacement.split(',')
                for token in shown_balls:
                    count, color = token.split()
                    count = int(count)
                    shown[color] = count
                best_bag = min_possible(best_bag, shown)
            total += power(best_bag)
    return total

if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = "input.txt"
    print(part1(input_file))
    print(part2(input_file))

