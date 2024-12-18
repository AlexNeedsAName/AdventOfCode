#!/usr/bin/env python3
import argparse
from aoc_util import dbg


def combo(machine, operand):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return machine.A
    elif operand == 5:
        return machine.B
    elif operand == 6:
        return machine.C
    elif operand == 7:
        print("AHHHHHHHH")
        return 0

def adv(machine, operand):
    machine.A = machine.A // (2**combo(machine,operand))
    machine.pc += 2

def bxl(machine, operand):
    dbg.print(f"Setting B to {machine.B} ^ {operand} = {machine.B ^ operand}")
    machine.B = machine.B ^ operand
    machine.pc += 2

def bst(machine, operand):
    machine.B = combo(machine, operand) % 8
    machine.pc += 2

def jnz(machine, operand):
    if machine.A == 0:
        machine.pc += 2
    else:
        machine.pc = operand

def bxc(machine, operand):
    machine.B = machine.B ^ machine.C
    machine.pc += 2

def out(machine, operand):
    machine.output.append(combo(machine, operand) % 8)
    machine.pc += 2

def bdv(machine, operand):
    machine.B = machine.A // (2**combo(machine,operand))
    machine.pc += 2

def cdv(machine, operand):
    machine.C = machine.A // (2**combo(machine,operand))
    machine.pc += 2


opcodes = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}

combo_opcodes = set((0,2,5,6,7))


class Machine:
    def __init__(self, A,B,C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program

        self.output = []
        self.pc = 0

        self.startA = A
        self.startB = B
        self.startC = C

    def run(self, quine=False):
        while self.pc <= len(self.program)-1:
            operator, operand = self.program[self.pc:self.pc+2]
            dbg.print('\n')
            dbg.print(opcodes[operator].__name__, operand if operator not in combo_opcodes else combo(self, operand))
            #input()
            opcodes[operator](self, operand)
            dbg.print(self)

            if quine and operator == 5:
                if self.output[-1] != self.program[len(self.output)-1]:
                    return False

        if quine:
            return self.output == self.program
        return self.output

    def reset(self):
        self.A = self.startA
        self.B = self.startB
        self.C = self.startC
        self.output = []
        self.pc = 0

    def __str__(self):
        return f"Register A: {self.A}\nRegister B: {self.B}\nRegister C: {self.C}\n\nProgram: {self.program}\n{' ' * (10 + 3 * self.pc)}^\nOutput: {self.output}"

    @classmethod
    def from_file(cls, file):
        registers = []
        for line in file:
            registers.append(int(line.strip().split()[-1]))
            if len(registers) >= 3:
                break
        file.readline()
        program = [int(token) for token in file.readline().strip().split()[-1].split(',')]
        return cls(*registers, program)


def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        machine = Machine.from_file(file)

    if part2:
        A = 0
        while True:
            machine.reset()
            machine.A = A
            result = machine.run(True)
            if result is not False:
                return A
            A += 1
            if A % 100000 == 0:
                print(A)

    dbg.print(machine)
    return ','.join(str(n) for n in machine.run())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

