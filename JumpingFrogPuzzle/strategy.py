class GraphBreadthFirst:
    def __init__(self):
        self.visited = set()

    def add_visited(self, state):
        self.visited.add(tuple(state))

    def select(self, new_nodes, fringe):
        new_fringe = new_nodes + fringe
        return [n for n in new_fringe if tuple(n.state) not in self.visited]


class GraphDepthFirst:
    def __init__(self):
        self.visited = set()

    def add_visited(self, state):
        self.visited.add(tuple(state))

    def select(self, new_nodes, fringe):
        new_fringe = fringe + new_nodes
        return [n for n in new_fringe if tuple(n.state) not in self.visited]


class GraphDepthLimitedFirst:
    def __init__(self, limit):
        self.visited = set()
        self.limit = limit

    def add_visited(self, state):
        self.visited.add(tuple(state))

    def select(self, new_nodes, fringe):
        new_fringe = fringe + new_nodes
        filtered_fringe = [n for n in new_fringe if tuple(n.state) not in self.visited]
        return [n for n in filtered_fringe if n.depth <= self.limit]


class AStar:
    def __init__(self, problem):
        self.problem = problem
        self.visited = set()

    def add_visited(self, state):
        self.visited.add(tuple(state))

    def select(self, new_nodes, fringe):
        new_fringe = fringe + new_nodes
        filtered_fringe = [n for n in new_fringe if tuple(n.state) not in self.visited]
        return sorted(filtered_fringe, key=lambda node: -(node.cost + self.problem.h(node.state)))
