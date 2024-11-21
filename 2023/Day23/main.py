#!/usr/bin/env python3
import argparse
from aoc_util import dbg, Point, CardinalDirection
import search


class HikingTrailSearch(search.SearchProblem):
    def __init__(self, start_state):
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state.isWinState()

    def getSuccessors(self, state):
        sucessors = state.generateSucessors()
#        input(sucessors)
#        print('\n=================================\n')
        return sucessors

    def getCostOfActions(self, actions):
        return len(actions)


class Board:
    def __init__(self, board):
        self.start = Point(board[0].find('.'), 0)
        self.end = Point(board[-1].find('.'), len(board)-1)
        self.board = board
        self.width = len(board[0])
        self.height = len(board)

    def at(self, point):
        x,y = point
        try:
            return self.board[y][x]
        except IndexError:
            return '#'

    @classmethod
    def from_file(cls, file):
        board = [line.strip() for line in file]
        return cls(board)

    def __str__(self):
        first = ['#' for i in range(len(self.board[0]))]
        last = ['#' for i in range(len(self.board[0]))]
        first[self.start.x] = 'S'
        last[self.end.x] = 'E'
        first = [''.join(first)]
        last = [''.join(last)]

        middle = self.board[1:-1]

        return '\n'.join(first + middle + last)


class HikingTrail:
    def __init__(self, board, position, visited):
        self.board = board
        self.position = position
        self.visited = frozenset(list(visited)+[self.position])

    def isWinState(self):
        return self.position.y == len(self.board.board) - 1

    def valid_directions(self):
        standing_on = self.board.at(self.position)
        if standing_on != '.':
            directions = [CardinalDirection.from_char(standing_on)]
        else:
            directions = CardinalDirection
        return directions

    def generateSucessors(self):
#        sucessors = [(HikingTrail(self.board, self.position.move(direction), self.visited), direction, 1) for direction in directions if self.board.at(self.position.move(direction)) != '#']
        sucessors = []
        for direction in self.valid_directions():
            new_position = self.position.move(direction)
            if self.board.at(new_position) == '#':
                continue
            if new_position in self.visited:
                continue
            sucessors.append((self.__class__(self.board, new_position, self.visited), direction, 1))
        return sucessors

    def __hash__(self):
        return hash(f'{hash(self.visited)} {self.position}')

    def __str__(self):
        result = [[c for c in row] for row in self.board.board]
        for x,y in self.visited:
            result[y][x] = 'O'
        result[self.board.start.y][self.board.start.x] = 'S'
        result[self.board.end.y][self.board.end.x] = 'E'
        return '\n'.join(''.join(line) for line in result)

    def __repr__(self):
        return str(self)

    @classmethod
    def from_file(cls, file):
        board = Board.from_file(file)
        return cls(board, board.start, frozenset())

class ClimbableHikingTrail(HikingTrail):
    def valid_directions(self):
        return CardinalDirection


class AdjGraphNode:
    def __init__(self, key):
        self.key = key
        self.adjacent_nodes = {}
        self.edge_costs = {}

    def add_edge(self, other, cost):
        self.adjacent_nodes[other.key] = other
        self.edge_costs[other.key] = cost

    def cost_to(self, other):
        return self.edge_costs[other.key]

    @property
    def edge_count(self):
        return len(self.adjacent_nodes)

    def remove_edge(self, other):
        del self.adjacent_nodes[other.key]
        del self.edge_costs[other.key]

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f"AdjGraphNode({str(self.key)})"

class AdjGraph:
    def __init__(self):
        self.nodes = {}

    def simplify(self):
        potential_simple_nodes = list(self.nodes.values())
        while len(potential_simple_nodes) > 0:
            node = potential_simple_nodes.pop(-1)
            if node.edge_count != 2:
                continue
            a,b = node.adjacent_nodes.values()
            a.add_edge(b, a.cost_to(node) + node.cost_to(b))
            b.add_edge(a, b.cost_to(node) + node.cost_to(a))
            a.remove_edge(node)
            b.remove_edge(node)
            del self.nodes[node.key]

    @classmethod
    def from_board(cls, board, climbable=True):
        graph = cls()
        first_node = None
        last_node = None
        for y in range(board.height):
            for x in range(board.width):
                pos = Point(x,y)
                if board.at(pos) != '#':
                    node = AdjGraphNode(pos)
                    if first_node is None:
                        first_node = node
                    last_node = node
                    graph.nodes[node.key] = node
                    # Only checking up and left because nodes to the right and down won't exist yet
                    for direction in [CardinalDirection.NORTH, CardinalDirection.WEST]:
                        other_pos = pos.move(direction)
                        if board.at(other_pos) != '#':
                            other_node = graph.nodes[other_pos]
                            node.add_edge(other_node, 1)
                            other_node.add_edge(node, 1)
        print(f"Graph has {len(graph.nodes)} nodes before simplify")
        graph.simplify()
        print(f"Graph has {len(graph.nodes)} nodes after")
        return graph, first_node, last_node

    def generate_all_paths(self, a, b, used=None):
        if used is None:
            used = [a]
        result = []
        for node in a.adjacent_nodes.values():
            if node == b:
                return [used + [b]]
            if node in used:
                continue
            result.extend(self.generate_all_paths(node,b,used+[node]))
        return result


def get_path_cost(path):
#    print(f"Path has {len(path)} nodes")
    return sum(a.edge_costs[b.key] for a,b in zip(path,path[1:]))

class AdjGraphSearch(search.SearchProblem):
    def __init__(self, start_state):
        self.start_state = start_state

    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state.isWinState()

    def getSuccessors(self, state):
        return state.generateSucessors()

    def getCostOfActions(self, actions):
        return sum(action[2] for action in actions)

class AdjGraphState:
    def __init__(self, position, visited, target):
        self.position = position
        self.visited = frozenset(list(visited) + [self.position])
#        print(f"{len(self.visited) = }")
        self.target = target

    def isWinState(self):
        return self.position == self.target

    def generateSucessors(self):
        sucessors = []
        for node in self.position.adjacent_nodes.values():
            if node in self.visited:
                continue
            sucessors.append((self.__class__(node, self.visited, self.target), node, self.position.edge_costs[node.key]))
        return sucessors

    def __hash__(self):
        return hash((self.visited, self.position))



def problem(input_file, part2=False):
    with open(input_file, 'r') as file:
        if not part2:
            start_state = HikingTrail.from_file(file)
        else:
            start_state = ClimbableHikingTrail.from_file(file)

    if part2:
        graph, start_node, end_node = AdjGraph.from_board(start_state.board)
#        start_state = AdjGraphState(start_node, [], end_node)
#        problem = AdjGraphSearch(start_state)
        all_paths = graph.generate_all_paths(start_node, end_node)
        print(f"there are {len(all_paths)} total paths")
        max_length = 0
        longest_path = None
        for path  in all_paths:
            length = get_path_cost(path)
            if length > max_length:
                max_length = length
                longest_path = path
        print(longest_path)
        return max_length
#        return max(get_path_cost(path) for path in all_paths)
    else:
        problem = HikingTrailSearch(start_state)
#    solutions = search.dfs(problem, find_all=True)
    solutions = search.astar(problem, find_all=True)
    print(solutions[-1])
    return solutions[-1].cost


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    dbg.set_level(args.verbose)

#    print(problem(args.filename))
    print(problem(args.filename, part2=True))

