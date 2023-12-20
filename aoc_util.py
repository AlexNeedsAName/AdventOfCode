import enum

digits = [str(i) for i in range(0,10)] + [chr(c) for c in range(ord('A'), ord('Z')+1)]

class Debugger:
    def __init__(self):
        self.debug_level = 0

    def set_level(self, level):
        self.debug_level = level

    def print(self, *args, level=1, **kwargs):
        if self.debug_level >= level:
            print(*args, **kwargs)

dbg = Debugger()

class Cols:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = [row[self.index] for row in self.data]
            self.index += 1
            return row
        except IndexError:
            raise StopIteration

def transpose(matrix):
    return [row for row in Cols(matrix)]


def string_distance(A, B):
    return sum(0 if a==b else 1 for a,b in zip(A,B))


def differences(A,B):
    return [i for i,(a,b) in enumerate(zip(A,B)) if a != b]


class RelativeDirection(enum.Enum):
    LEFT = -1
    FORWARDS = 0
    RIGHT = 1
    BACKWARDS = 2


class CardinalDirection(enum.Enum):
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

    @staticmethod
    def from_char(char):
        if char == 'U' or char == 'N':
            return CardinalDirection.NORTH
        elif char == 'D' or char == 'S':
            return CardinalDirection.SOUTH
        elif char == 'L' or char == 'W':
            return CardinalDirection.WEST
        elif char == 'R' or char == 'E':
            return CardinalDirection.EAST


class Point(tuple):
    def __new__(self, x, y):
        return tuple.__new__(Point, (x,y))

    def move(self, direction):
        x,y = self
        if direction == CardinalDirection.NORTH:
            y -= 1
        elif direction == CardinalDirection.EAST:
            x += 1
        elif direction == CardinalDirection.SOUTH:
            y += 1
        elif direction == CardinalDirection.WEST:
            x -= 1
        return Point(x,y)
