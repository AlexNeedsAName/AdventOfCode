#!/usr/bin/env python3
import argparse

DEBUG=0
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class Label(str):
    def __hash__(self):
        value = 0
        for c in self:
            value += ord(c)
            value *= 17
            value = value % 256
        dbg_print(f'Hash of \'{self}\' is {value}', level=2)
        return value


class HashMap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.boxes = [[] for i in range(capacity)]

    def _get_box(self, key):
        return self.boxes[hash(key) % self.capacity]

    def __getitem__(self, key):
        box = self._get_box(key)
        keys = [key for key,value in box]
        try:
            return box[keys.index(key)][1]
        except ValueError:
            raise KeyError(f"Key {key} was not in map")

    def __setitem__(self, key, value):
        box = self._get_box(key)
        keys = [key for key,value in box]
        try:
            box[keys.index(key)] = (key, value)
        except ValueError:
            box.append((key, value))

    def pop(self, key):
        box = self._get_box(key)
        keys = [key for key,value in box]
        try:
            return box.pop(keys.index(key))[1]
        except ValueError:
            raise KeyError(f"Key {key} was not in map")

    def __delitem__(self, key):
        try:
            self.pop(key)
        except KeyError:
            pass

    def value(self):
        total = 0
        for i,box in enumerate(self.boxes):
            total += sum((i+1) * (j+1) * value for j,(label,value) in enumerate(box))
        return total

    def __str__(self):
        results = []
        for i,box in enumerate(self.boxes):
            line = ' '.join(f'[{label} {value}]' for label,value in box)
            if len(line) > 0:
                results.append(f'Box {i}: {line}')
        return '\n'.join(results)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        tokens = file.readline().strip().split(',')

    if not part2:
        return sum(hash(Label(token)) for token in tokens)
    else:
        map = HashMap(256)
        for token in tokens:
            if token[-1] == '-':
                key = Label(token[:-1])
                del map[key]
            else:
                key,value = token.split('=')
                map[Label(key)] = int(value)
            dbg_print(f'After "{token}"\n{map}\n')
        return map.value()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

