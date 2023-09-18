from node import Node
from strategy import *


class ThreeSearch:

    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy
        self.fringe = []

    def run(self):
        node = Node(state=self.problem.initial_state, parent=None, action=None, cost=0, depth=0)

        while True:
            if self.problem.goal_test(node.state):
                return node.path()

            next_nodes = [node.expand(state=s, action=a, cost=1) for s, a in self.problem.successors(node.state)]

            self.fringe = self.strategy.select(new_nodes=next_nodes, fringe=self.fringe)

            if len(self.fringe) == 0:
                return False

            node = self.fringe.pop()
            print(f"We picked {node.state} from the fringe")
            self.strategy.add_visited(node.state)


class IterativeDeepeningSearch:

    def __init__(self, problem):
        self.problem = problem
        self.fringe = []

    def run(self, limit=0):
        strategy = GraphDepthLimitedFirst(limit=limit)
        node = Node(state=self.problem.initial_state, depth=0, cost=0, action=None, parent=None)
        while True:
            if self.problem.goal_test(node.state):
                return node.path()

            new_nodes = [node.expand(state=s, action=a) for s, a in self.problem.successors(node.state)]

            self.fringe = strategy.select(fringe=self.fringe, new_nodes=new_nodes)

            if len(self.fringe) == 0:
                limit += 1
                return self.run(limit)
            node = self.fringe.pop()
            strategy.add_visited(node.state)


