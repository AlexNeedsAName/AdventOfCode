#!/usr/bin/env python3
import argparse
from progressbar import progressbar

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)



def part1(input_file):
    with open(input_file, 'r') as file:
        race_times = [] #ms
        race_distances = [] #mm

        times = [int(token) for token in file.readline().split(':')[-1].strip().split()]
        distances = [int(token) for token in file.readline().split(':')[-1].strip().split()]

        prod = 1
        for time, record_distance in zip(times, distances):
            ways_to_beat_record = 0
            for i in progressbar(range(time)):
                # spend i seconds accelerating
                speed = i
                time_left = time-i
                distance = speed * time_left
                if distance > record_distance:
                    ways_to_beat_record+=1
            prod *= ways_to_beat_record

    return prod


def part2(input_file):
    with open(input_file, 'r') as file:
        time = int(file.readline().split(':')[-1].replace(' ', ''))
        record_distance = int(file.readline().split(':')[-1].replace(' ', ''))

        count = 0
        for i in range(time):
            speed = i
            time_left = time-i
            distance = speed * time_left
            if distance > record_distance:
                count += 1

    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))
    print(part2(args.filename))

