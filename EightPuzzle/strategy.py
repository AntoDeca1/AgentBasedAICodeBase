from EightPuzzle.problem import EightPuzzle


class BreadthFirst:

    def __init__(self, visited):
        self.visited = set()

    def select(self, fringe, new_nodes):
        return new_nodes + fringe

    def add_visted(self, state):
        pass


class GraphBreadthFirst:
    def __init__(self):
        self.visited = set()

    def select(self, fringe, new_nodes):
        nodes_filtered = [n for n in new_nodes if tuple(n.state.flatten()) not in self.visited]
        return nodes_filtered + fringe

    def add_visited(self, state):
        self.visited.add(tuple(state.flatten()))


class DepthFirst:
    def __init__(self):
        self.visited = set()

    def select(self, fringe, new_nodes):
        return fringe + new_nodes

    def add_visted(self, state):
        pass


class GraphDepthLimitedSearch:
    def __init__(self, limit):
        self.visited = set()
        self.limit = limit

    def select(self, fringe, new_nodes):
        new_fringe = fringe + new_nodes
        new_fringe_filtered = [n for n in new_fringe if tuple(n.state.flatten()) not in self.visited]
        return [n for n in new_fringe_filtered if n.depth <= self.limit]

    def add_visted(self, state):
        self.visited.add(tuple(state.flatten()))


class AStar:
    def __init__(self, problem):
        self.visited = set()
        self.problem = problem

    def select(self, fringe, new_nodes):
        filtered_nodes = [n for n in new_nodes if tuple(n.state.flatten()) not in self.visited]
        new_fringe = fringe + filtered_nodes
        new_fringe_sorted = sorted(new_fringe, key=lambda el: -(el.cost + self.problem.h(el.state)))
        return new_fringe_sorted

    def add_visited(self, state):
        self.visited.add(tuple(state.flatten()))
