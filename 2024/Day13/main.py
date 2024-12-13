#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point

class ClawMachine:
    def __init__(self, buttons, prize, costs):
        self.buttons = buttons
        self.prize = prize
        self.costs = costs

    def find_min_cost_bad(self, max_presses=100):
        a_presses = 0
        while a_presses < max_presses:
            base = self.buttons['A'] * a_presses
            if base.x > self.prize.x or base.y > self.prize.y:
                break
            b_presses = 0
            while b_presses < max_presses:
                pos = base + (self.buttons['B'] * b_presses)
                dbg.print(f'A * {a_presses} + B * {b_presses} = {pos}. Prize = {self.prize}')
                if pos.x > self.prize.x or pos.y > self.prize.y:
                    break
                if pos == self.prize:
                    return self.costs['A'] * a_presses + self.costs['B'] * b_presses, {'A': a_presses, 'B': b_presses}
                b_presses += 1
            a_presses += 1
        return float('inf'), {}


    # this only works if a and b are linearly independant though, since it doesn't try to optimize for cost at all
    def find_min_cost(self):
        xa,ya = self.buttons['A']
        xb,yb = self.buttons['B']
        xp,yp = self.prize
        b = (ya*xp-xa*yp)/(ya*xb-xa*yb)
        a = (yp-yb*b)/ya
        if a % 1 != 0 or b %1 != 0:
            return float('inf'), {}
        a = int(a)
        b = int(b)
        return self.costs['A'] * a + self.costs['B'] * b, {'A': a, 'B': b}

#    def find_min_cost(self, target=None, max_presses=100):
#        if target is None:
#            target = self.prize
#        if target == Point(0,0):
#            return (0, [])
#        elif max_presses == 0 or target.x < 0 or target.y < 0:
#            return (float('inf'), [])
#        options = []
#        for button,offset in self.buttons.items():
#            cost,presses = self.find_min_cost(target-offset, max_presses-1)
#            options.append((cost + self.costs[button], presses + [button]))
#        return min(options)

    @classmethod
    def from_file(cls, file, costs, part2):
        buttons = {}
        machines = []
        for line in file:
            tokens = line.strip().split()
            if len(tokens) == 0:
                continue
            elif tokens[0] == "Button":
                buttons[tokens[1][:-1]] = Point(int(tokens[2].split('+')[-1][:-1]), int(tokens[3].split('+')[-1]))
            elif tokens[0] == "Prize:":
                prize = Point(int(tokens[1].split('=')[-1][:-1]), int(tokens[2].split('=')[-1]))
                if part2:
                    prize = prize + Point(10000000000000, 10000000000000)
                machines.append(cls(buttons, prize, costs))
                buttons = {}
        return machines

    def __repr__(self):
        return f"{self.__class__.__name__}(buttons={self.buttons}, prize={self.prize})"

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        machines = ClawMachine.from_file(file, {'A': 3, 'B': 1}, part2)

    total = 0
    for machine in machines:
        cost, presses = machine.find_min_cost()
        dbg.print(f"Machine {machine} costs {cost} with inputs {presses}")
        if cost < float('inf'):
            total += cost
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

    print(problem(args.filename))
    print(problem(args.filename, part2=True))

