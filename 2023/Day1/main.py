#!/usr/bin/env python

import sys

digit_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def part1(input_file):
    calibration_values = []
    with open(input_file, 'r') as file:
        for line in file:
            first = None
            last = None
            for char in line:
                if char.isdigit():
                    first = int(char)
                    break

            for char in line[::-1]:
                if char.isdigit():
                    last = int(char)
                    break

            calibration_values.append(first * 10 + last)

    print(calibration_values)
    print(sum(calibration_values))

def part2(input_file):
    calibration_values = []
    with open(input_file, 'r') as file:
        for line in file:
            first = None
            last = None

            for i in range(len(line)):
                if line[i].isdigit():
                    first = int(line[i])
                    #print(line[i])
                    break
                for j,digit in enumerate(digit_strings):
                    if line[i:].startswith(digit):
                        first = j+1
                        #print(digit)
                        break
                if first != None:
                    break

            for i in range(len(line)):
                if line[-i-1].isdigit():
                    last = int(line[-i-1])
                    #print(line[-i-1])
                    break
                for j,digit in enumerate(digit_strings):
                    if line[len(line)-i-1:].startswith(digit):
                        last = j+1
                        #print(digit)
                        break
                if last != None:
                    break
            #print(line)
            calibration_values.append(first * 10 + last)
            #print(calibration_values[-1])

    print(calibration_values)
    print(sum(calibration_values))


if __name__ == "__main__":
    print("Part 1:")
    part1(sys.argv[1])

    print("Part 2:")
    part2(sys.argv[1])
