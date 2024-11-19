#!/usr/bin/env python3
import argparse
from aoc_util import dbg
from collections import defaultdict, deque
from enum import Enum

class Level(Enum):
    LOW = 0
    HIGH = 1

    def invert(self):
        if self == Level.LOW:
            return Level.HIGH
        return Level.LOW

    def __str__(self):
        if self == Level.LOW:
            return 'low'
        else:
            return 'high'

LOW = Level.LOW
HIGH = Level.HIGH
OFF = LOW
ON = HIGH

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        sim = Sim(file)

    if not part2:
        for i in range(1000):
            sim.push_the_button()
            sim.run()
        return sim.score()
    else:
        while len(sim.conjunction_cycles) < 4:
            sim.push_the_button()
            sim.run()
        result = 1
        for key,value in sim.conjunction_cycles.items():
            result *= value
        return result



class Sim:
    def __init__(self, file):
        self.pulse_count = {LOW: 0, HIGH: 0}
        self.press_count = 0
        self.conjunction_cycles = {}
        self.modules = {}
        self.pulse_queue = deque()
        links = []
        self.rx_low = False
        for line in file:
            module = Module.from_line(line, self)
            print(module)
            for dst in module.destinations:
                links.append((module.name, dst))
        for src, dst in links:
            try:
                self.modules[dst].register_sender(src)
            except KeyError:
                pass

    def score(self):
        dbg.print(self.pulse_count)
        return self.pulse_count[LOW] * self.pulse_count[HIGH]

    def tick(self):
        dst, pulse, src = self.pulse_queue.popleft()
        self.pulse_count[pulse] += 1
        dbg.print(f'{src} -{pulse}-> {dst}')

        if dst == 'rx' and pulse == LOW:
            self.rx_low = True
        elif dst == 'zh' and pulse == HIGH:
            if src not in self.conjunction_cycles.keys():
                self.conjunction_cycles[src] = self.press_count
                print(self.conjunction_cycles)
        try:
            self.modules[dst].get_pulse(pulse, src)
        except KeyError:
            pass

    def push_the_button(self):
        dbg.print("Pushing the button")
        self.press_count += 1
        self.pulse_queue.append(('broadcaster', LOW, 'button'))

    def run(self):
        dbg.print()
        while len(self.pulse_queue) > 0:
            self.tick()



class Module:
    def __init__(self, name, destinations, sim):
        self.name = name
        self.destinations = destinations
        self.sim = sim
        self.sim.modules[name] = self

    def register_sender(self, sender):
        pass

    def get_pulse(self, pulse, sender):
        pass

    def send_pulse(self, pulse):
        for dst in self.destinations:
            self.sim.pulse_queue.append((dst, pulse, self.name))

    @classmethod
    def from_line(cls, line, sim):
        name, arrow, *dsts = line.strip().replace(',', '').split()

        module = None
        if name[0] == '%':
            module = FlipFlop(name[1:], dsts, sim)
        elif name[0] == '&':
            module = Conjunction(name[1:], dsts, sim)
        elif name == 'broadcaster':
            module = Broadcaster(name, dsts, sim)
        return module

    def __str__(self):
        return f'{self.name} -> {", ".join(dst for dst in self.destinations)}'

class FlipFlop(Module):
    def __init__(self, name, destinations, sim):
        super().__init__(name, destinations, sim)
        self.state = OFF

    def get_pulse(self, pulse, sender):
        if pulse == LOW:
            self.state = self.state.invert()
            self.send_pulse(self.state)

    def __str__(self):
        return f'%{super().__str__()}'


class Conjunction(Module):
    def __init__(self, name, destinations, sim):
        super().__init__(name, destinations, sim)
        self.memory = {}

    def register_sender(self, sender):
        self.memory[sender] = LOW

    def get_pulse(self, pulse, sender):
        self.memory[sender] = pulse
        #print(f'{self.name} got a {pulse} pulse from {sender}. State is now {self.memory}')
        if LOW in self.memory.values():
            self.send_pulse(HIGH)
        else:
            self.send_pulse(LOW)

    def __str__(self):
        return f'&{super().__str__()}'


class Broadcaster(Module):
    def get_pulse(self, pulse, sender):
        self.send_pulse(pulse)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))

