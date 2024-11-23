#!/usr/bin/env python3
import argparse
from aoc_util import dbg
from intcode import IntcodeVM

def problem(input_file, part2=False):
    if not part2:
        vm = IntcodeVM.from_file(input_file)
        vm.dbg = dbg.debug_level
        vm.memory.set(1, 12)
        vm.memory.set(2, 2)
        if vm.dbg:
            print(vm)
        vm.run()
        return vm.memory.get(0)

    target = 19690720
    for noun in range(100):
        for verb in range(100):
            vm = IntcodeVM.from_file(input_file)
            print(f"Trying {noun = }; {verb = };")
            vm.dbg = dbg.debug_level
            vm.memory.set(1, noun)
            vm.memory.set(2, verb)
            vm.core_dump_enabled = False
            vm.run()
            if vm.memory.get(0) == target:
                return 100 * noun + verb
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))
    print(f"{dbg.debug_level = }")

