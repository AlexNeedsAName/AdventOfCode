import enum
from collections import defaultdict
import itertools
import sys

if not hasattr(itertools, 'batched'):
    itertools.batched = lambda iterable, batch_size: zip(*(iterable[i::batch_size] for i in range(batch_size)))


class IntcodeException(Exception):
    pass

class OutOfBoundsException(IntcodeException):
    pass

class InvalidOpcode(IntcodeException):
    pass


class Instruction:
    def __init__(self, memory, pc):
        full_opcode = memory.get(pc)
        self.op = Opcode.from_code(full_opcode % 100)
        self.is_immediate = [full_opcode % (10**(x+3)) // (10**(x+2)) for x in range(self.op.potential_indirects)]
        self.is_immediate.extend([True] * (self.op.param_count-self.op.potential_indirects))
        self.parameters = [memory.get(pc+i) for i in range(1,self.op.param_count+1)]

    def execute(self, machine):
        parameters = [param if immediate else machine.memory.get(addr=param) for param,immediate in zip(self.parameters, self.is_immediate)]
        self.op.function(machine, parameters)
        machine.pc += self.op.param_count+1

    def __str__(self):
        result = [self.op.name]
        result.append(', '.join(f'{"" if immediate else "*"}{param}' for param,immediate in zip(self.parameters, self.is_immediate)))
        return " ".join(result)

def nop(state):
    pass


class Opcode:
    opcodes = {}
    def __init__(self, name, code, param_count=0, potential_indirects=0, function=nop):
        self.name = name
        self.code = code
        self.param_count = param_count
        self.potential_indirects = potential_indirects
        self.function = function
        setattr(self.__class__, self.name, self)
        self.__class__.opcodes[self.code] = self

    def __repr__(self):
        return f"<Opcode.{self.name}: {self.code}>"

    @classmethod
    def from_code(cls, code):
        try:
            return cls.opcodes[code]
        except KeyError:
            raise InvalidOpcode(f"Invalid opcode: {code}")

Opcode("ADD", code=1, param_count=3, potential_indirects=2, function=lambda vm, params: vm.memory.set(params[2], params[0] + params[1]))
Opcode("MUL", code=2, param_count=3, potential_indirects=2, function=lambda vm, params: vm.memory.set(params[2], params[0] * params[1]))
Opcode("HALT", code=99, function=lambda vm, params: vm.halt())

#class Opcode(enum.Enum):
#    ADD   = 1
#    MUL   = 2
#    READ  = 3
#    WRITE = 4
#    HALT  = 99

class Memory:
    def __init__(self, data):
        self.data = data

    def set(self, addr, value):
        try:
            self.data[addr] = value
        except IndexError:
            raise OutOfBoundsException(f"Write error: {addr} is out of bounds")

    def get(self, addr):
        try:
            return self.data[addr]
        except IndexError:
            raise OutOfBoundsException(f"Read error: {addr} is out of bounds")

    def __str__(self):
        return "\n".join(f"{','.join(str(item) for item in batch)}," for batch in itertools.batched(self.data, 4))


class IntcodeVM:
    def __init__(self, memory):
        self.tick_count = 0
        self.pc = 0
        self.memory = memory
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.is_halted = False
        self.core_dump_enabled = True
        self.dbg = 0

    def halt(self):
        self.is_halted = True

    def get_params(self, count):
        return self.memory[self.pc+1:self.pc+1+count]

    def tick(self):
        self.tick_count += 1
        instruction = Instruction(self.memory, self.pc)
        if self.dbg:
            print(str(instruction))
        instruction.execute(self)

    def run(self):
        while not self.is_halted:
            try:
                self.tick()
                if self.dbg >= 2:
                    print(self)
            except IntcodeException as e:
                print(f"Intcode program exception: {e}")
                if self.core_dump_enabled:
                    print(self)
                self.halt()
        print("Program halted")

    def __str__(self):
        result = []
        result.append(f"tick {self.tick_count}")
        result.append(f"{self.pc = }; {self.is_halted = };")
        result.append(f"memory:\n{str(self.memory)}")
        result.append('\n')
        return '\n'.join(result)

    @classmethod
    def from_file(cls, file):
        program = []
        with open(file, 'r') as file:
            for line in file:
                program.extend(int(token) for token in line.split(','))
        return cls(Memory(program))
