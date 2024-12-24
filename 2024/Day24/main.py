#!/usr/bin/env python3
import argparse
from aoc_util import dbg

class Wire:
    def __init__(self, name=None):
        self.name = name
        self.state = None
        self.dependencies = set()
        self.sources = set()

    def add_dep(self, dep):
        self.dependencies.add(dep)

    def add_source(self, source):
        self.sources.add(source)

    def set(self, state):
        self.state = bool(state)
        for dep in self.dependencies:
            dep.update()

    def get(self):
        return self.state

    def __str__(self):
        val = "Undefined" if self.state is None else int(self.state)
        return f'{self.name}: {val}'

class Gate:
    def __init__(self, input_a, input_b, output):
        self.a = input_a
        self.b = input_b
        self.out = output

        self.a.add_dep(self)
        self.b.add_dep(self)
        self.out.add_source(self.a)
        self.out.add_source(self.b)

    @staticmethod
    def op(a,b):
        pass

    def update(self):
        a = self.a.get()
        b = self.b.get()
        out = self.out.get()
        if out is not None or a is None or b is None:
            return False

        self.out.set(self.op(a, b))

        return True

    def __str__(self):
        return f"{self.a.name} {self.__class__.__name__} {self.b.name} -> {self.out.name}"


class XOR(Gate):
    @staticmethod
    def op(a,b):
        return a ^ b

class OR(Gate):
    @staticmethod
    def op(a,b):
        return a or b

class AND(Gate):
    @staticmethod
    def op(a,b):
        return a and b


str_to_gate = {
    "AND": AND,
    "XOR": XOR,
    "OR": OR,
}


class Circuit:
    def __init__(self, wires, gates):
        self.wires = wires
        self.gates = gates
        self.num_size = sum(1 if name[0] == 'z' else 0 for name in self.wires.keys()) -1

    def reset(self):
        for wire in self.wires.values():
            wire.state = None

    def setup(self, x, y):
        self.reset()
        self.set_num('x', x)
        self.set_num('y', y)

    @classmethod
    def from_file(cls, file):
        wires = {}
        gates = []
        for line in file:
            line = line.strip()
            if len(line) == 0:
                break
            name, value = line.split(':')
            wire = Wire(name)
            wire.set(bool(int(value)))
            wires[name] = wire

        for line in file:
            line = line.strip()
            a, op, b, _, dst = line.split()

            try:
                A = wires[a]
            except KeyError:
                A = Wire(a)
                wires[a] = A
            try:
                B = wires[b]
            except KeyError:
                B = Wire(b)
                wires[b] = B
            try:
                DST = wires[dst]
            except KeyError:
                DST = Wire(dst)
                wires[dst] = DST

            gates.append(str_to_gate[op](A, B, DST))

        return cls(wires, gates)

    def extract_num(self, prefix):
        result = 0
        for i in range(self.num_size + (1 if prefix == 'z' else 0)):
            result += (self.wires[f'{prefix}{i:02}'].get() << i)
        return result

    def set_num(self, prefix, value):
        for i in range(self.num_size):
            self.wires[f'{prefix}{i:02}'].state = (value >> i) & 1

    def sim(self):
        while True:
            changed = False
            for gate in self.gates:
                if gate.update():
                    changed = True
            if not changed:
                break
            dbg.print(self)

        return self.extract_num('z')

    def get_wire_tree(self, wire):
        result = wire.sources.copy()
        for source in wire.sources:
            result = result.union(self.get_wire_tree(source))
        return result

    def __str__(self):
        result = []

        for wire in self.wires.values():
            result.append(str(wire))
        result.append('')

        for gate in self.gates:
            result.append(str(gate))

        return '\n'.join(result)



def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        problem = Circuit.from_file(file)

    if not part2:
        dbg.print(problem)
        result = problem.sim()
        dbg.print(problem)
        return result

    else:
        x_init = problem.extract_num('x')
        y_init = problem.extract_num('y')
        print(f"x = {x_init}")
        print(f"y = {y_init}")
        problem.sim()
        print(f"z = {problem.extract_num('z')}")

        problem_bits = set()
        for i in range(problem.num_size):
            val = 1 << i
            problem.setup(val, 0)
            z = problem.sim()
            if z != val:
                print(f"problem in bit {i} with x{i} set to 1")
                problem_bits.add(i)
            problem.setup(0, val)
            z = problem.sim()
            if z != val:
                print(f"problem in bit {i} with y{i} set to 1")
                problem_bits.add(i)

#        for bit in problem_bits:
#            print(f"Problem bit z{bit} consists of:")
#            print(problem.wires[f'z{bit:02}'].sources)
#            for wire in problem.get_wire_tree(problem.wires[f'z{bit:02}']):
#                print(wire)
#            print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

