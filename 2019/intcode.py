import enum
from collections import defaultdict
import itertools

if not hasattr(itertools, 'batched'):
    itertools.batched = lambda iterable, batch_size: zip(*(iterable[i::batch_size] for i in range(batch_size)))


class Opcode(enum.Enum):
    ADD = 1
    MUL = 2
    HALT = 99

class IntcodeException(Exception):
    pass

class OutOfBoundsException(IntcodeException):
    pass


class IntcodeVM:
    def __init__(self, code):
        self.tick_count = 0
        self.pc = 0
        self.memory = code
        self.halt = False
        self.core_dump_enabled = True
        self.dbg = False

    def get_params(self, count):
        return self.memory[self.pc+1:self.pc+1+count]

    def set(self, dst, value):
        try:
            self.memory[dst] = value
        except IndexError:
            raise OutOfBoundsException(f"Write error: {dst} is out of bounds")

    def get(self, src):
        try:
            return self.memory[src]
        except IndexError:
            raise OutOfBoundsException(f"Read error: {src} is out of bounds")

    def tick(self):
        self.tick_count += 1
        op = Opcode(self.memory[self.pc])
        if op == Opcode.ADD:
            a,b,dst = self.get_params(3)
            self.set(dst, self.get(a) + self.get(b))
            self.pc += 4
        elif op == Opcode.MUL:
            a,b,dst = self.get_params(3)
            self.set(dst, self.get(a) * self.get(b))
            self.pc += 4
        elif op == Opcode.HALT:
            self.halt = True

    def run(self):
        while not self.halt:
            try:
                self.tick()
                if self.dbg:
                    print(self)
            except IntcodeException as e:
                print(f"Intcode program exception: {e}")
                if self.core_dump_enabled:
                    print(self)
                self.halt = True
        print("Program halted")

    def __str__(self):
        result = []
        result.append(f"tick {self.tick_count}")
        result.append(f"{self.pc = }; {self.halt = };")
        result.append(f"memory:")
        result.extend(f"{','.join(str(item) for item in batch)}," for batch in itertools.batched(self.memory, 4))
        result.append('\n')
        return '\n'.join(result)

    @classmethod
    def from_file(cls, file):
        program = []
        with open(file, 'r') as file:
            for line in file:
                program.extend(int(token) for token in line.split(','))
        return cls(program)
