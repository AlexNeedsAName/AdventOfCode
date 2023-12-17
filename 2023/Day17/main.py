#!/usr/bin/env python3
import argparse
import search
from enum import Enum

DEBUG=0
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


class RelativeDirection(Enum):
    LEFT = -1
    FORWARDS = 0
    RIGHT = 1
    BACKWARDS = 2


class CardinalDirection(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn(self, relative_direction):
        return CardinalDirection((self.value + relative_direction.value) % 4)

    def as_char(self):
        if self == CardinalDirection.NORTH:
            return '^'
        elif self == CardinalDirection.EAST:
            return '>'
        elif self == CardinalDirection.SOUTH:
            return 'v'
        elif self == CardinalDirection.WEST:
            return '<'


class LavaPoolSearch(search.SearchProblem):
    def __init__(self, start_state):
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state.isWinState()

    def getSuccessors(self, state):
        return state.generateSucessors()

    def getCostOfActions(self, actions):
        return len(actions)


class Crucible:
    def __init__(self, board, position, facing, max_forwards):
        self.board = board
        self.position = position
        self.facing = facing
        self.max_forwards = max_forwards

    def isWinState(self):
        return (len(self.board[0])-1, len(self.board)-1) == self.position

    def generateSucessors(self):
        sucessors = []
        for direction in [RelativeDirection.LEFT, RelativeDirection.FORWARDS, RelativeDirection.RIGHT]:
            try:
                next = self.go(direction)
                x,y = next.position
                sucessors.append((next, direction, int(self.board[y][x])))
            except ValueError:
                pass
        return sucessors

    def go(self, direction):
        if direction == RelativeDirection.FORWARDS:
            max_forwards = self.max_forwards -1
            if max_forwards < 0:
                raise ValueError(f'Can not go forward again')
        else:
            max_forwards = 2

        facing = self.facing.turn(direction)
        x,y = self.position
        if facing == CardinalDirection.NORTH:
            y -= 1
        elif facing == CardinalDirection.SOUTH:
            y += 1
        elif facing == CardinalDirection.EAST:
            x += 1
        elif facing == CardinalDirection.WEST:
            x -= 1
        else:
            raise ArgumentError(f'Invalid direction {direction}')

        if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board):
            raise ValueError(f'New position {(x,y)} would be out of bounds')

        return Crucible(self.board, (x,y), facing, max_forwards)

    def __hash__(self):
        return hash(f'{self.position}, {self.facing}, {self.max_forwards}')

    def __eq__(self, other):
        return hash(self) == hash(other)

    def show_path(self, solution):
        chars = [[c for c in line] for line in  self.board]
        state = self
        for action in solution:
            c = state.facing.as_char()
            x,y = state.position
            chars[y][x] = c
            state = state.go(action)

        return '\n'.join(''.join(line) for line in chars)

class UltraCrucible(Crucible):

    def go(self, direction):
        if direction == RelativeDirection.FORWARDS:
            max_forwards = self.max_forwards -1
            if max_forwards < 0:
                raise ValueError(f'Can not go forward again')
        else:
            if self.max_forwards > 10-4:
                raise ValueError(f'Can not go turn yet')
            max_forwards = 9

        facing = self.facing.turn(direction)
        x,y = self.position
        if facing == CardinalDirection.NORTH:
            y -= 1
        elif facing == CardinalDirection.SOUTH:
            y += 1
        elif facing == CardinalDirection.EAST:
            x += 1
        elif facing == CardinalDirection.WEST:
            x -= 1
        else:
            raise ArgumentError(f'Invalid direction {direction}')

        if x < 0 or x >= len(self.board[0]) or y < 0 or y >= len(self.board):
            raise ValueError(f'New position {(x,y)} would be out of bounds')

        return UltraCrucible(self.board, (x,y), facing, max_forwards)

    def isWinState(self):
        return (len(self.board[0])-1, len(self.board)-1) == self.position and self.max_forwards <= 10-4

def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        board = [line.strip() for line in file]

    if not part2:
        start_state = Crucible(board, position=(0,0), facing=CardinalDirection.EAST, max_forwards=3)
    else:
        #TODO: This doesn't work anymore because of the restriction that it must be moving in the same direction 4 times before turning
        # Should be able to fix it by adding a second variable "until_can_turn" or something so we can set that to 0 for the start state
        start_state = UltraCrucible(board, position=(0,0), facing=CardinalDirection.SOUTH, max_forwards=10)
    problem = LavaPoolSearch(start_state)
    solution = search.astar(problem, find_all=False)

    print(start_state.show_path(solution))

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))

