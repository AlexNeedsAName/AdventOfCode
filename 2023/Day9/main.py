#!/usr/bin/env python3
import argparse

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)

def print_history(history,level=1):
    i = 0
    spacing = 4
    dbg_print('  ' * i + ''.join(f'{num:>{spacing}}' for num in history[0]).strip(), level=level)
    i += len(str(history[0][0]))-1
    for sequence in history[1:]:
        i+=spacing//2
        dbg_print(' ' * i + ''.join(f'{num:>{spacing}}' for num in sequence).strip(), level=level)

def part1(input_file):
    results1 = []
    results2 = []
    with open(input_file, 'r') as file:
        for line in file:
            history = [[int(token) for token in line.strip().split()]]
            while True:
                sequence = history[-1]
                derivitive = [b - a for a,b in zip(sequence, sequence[1:])]
                history.append(derivitive)
                if max(derivitive) == min(derivitive) == 0:
                    break

            history[-1].extend((0,0))
            for i in range(len(history)-2, -1, -1):
                history[i].append(history[i][-1] + history[i+1][-1])

                history[i].insert(0, history[i][0] - history[i+1][0])
#                dbg_print(f'{history[i][1]} - {history[i+1][0]} = {history[i][0]}')


            results1.append(history[0][-1])
            results2.append(history[0][0])

            print_history(history)
            dbg_print('')

    return sum(results1), sum(results2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename))

