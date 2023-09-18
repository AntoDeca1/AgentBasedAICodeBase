from EightPuzzle.node import Node
from EightPuzzle.strategy import *


class ThreeSearch:

    def __init__(self, problem, strategy):
        self.problem = problem
        self.strategy = strategy
        self.fringe = []

    def run(self):
        node = Node(state=self.problem.initial_state, depth=0, parent=None, cost=0, action=None)
        num_steps = 1
        while True:
            if self.problem.goal_test(node.state):
                return node.path()

            new_nodes = [node.expand(state=state, action=action, cost=1) for state, action in
                         self.problem.successors(node.state)]
            self.fringe = self.strategy.select(self.fringe, new_nodes)
            if len(self.fringe) == 0:
                return []
            node = self.fringe.pop()
            print(f"-----We moved to----\n {node.state}\n at step {num_steps}")
            num_steps += 1
            self.strategy.add_visited(node.state)


class IterativeDeepiningSearch:
    def __init__(self, problem):
        self.problem = problem
        self.fringe = []

    def run(self, limit=0):
        """
        With the iterative deepening im forced to use DepthLimited search
        :param limit:
        :return:
        """
        strategy = GraphDepthLimitedSearch(limit=limit)
        node = Node(state=self.problem.initial_state, cost=0, parent=None, depth=0, action=None)

        while True:
            if self.problem.goal_test(node.state):
                return node.path()
            new_nodes = [node.expand(s, action=a, cost=1) for s, a in self.problem.successors(node.state)]
            self.fringe = strategy.select(self.fringe, new_nodes)
            if len(self.fringe) == 0:
                limit += 1
                return self.run(limit)
            node = self.fringe.pop()
            strategy.add_visted(node.state)


class IterativeDeepiningAStar:
    def __init__(self, problem):
        self.problem = problem
        self.fringe = []

    def run(self, threshold=1):

        node = Node(state=self.problem.initial_state, depth=0, parent=None, cost=0, action=None)
        strategy = AStar(problem=self.problem)

        while True:
            if self.problem.goal_test(node.state):
                print(f"Solution-found-at-threshold-{threshold}")
                return node.path()

            new_nodes = [node.expand(state=s, action=a, cost=1) for s, a in self.problem.successors(node.state)]

            self.fringe = strategy.select(fringe=self.fringe, new_nodes=new_nodes)

            min_f = min([(node.cost + self.problem.h(node.state)) for node in self.fringe])

            if min_f > threshold:
                return self.run(threshold=min_f)

            node = self.fringe.pop()
            strategy.add_visited(node.state)


class BidirectionalSearch:
    def __init__(self, problem, strategy_fw, strategy_bw):
        self.problem = problem
        self.strategy_fw = strategy_fw
        self.strategy_bw = strategy_bw
        self.fringe_fw = []
        self.fringe_bw = []
        self.reached_fw = {}
        self.reached_bw = {}

    def join(self, node_fw, node_bw, reverse=True):
        path_fw = node_fw.path()
        path_bw = node_bw.path()
        if reverse == True:
            path_bw = [self.problem.reverse_action(action) for action in path_bw]
            return path_fw + list(reversed(path_bw))

    def run(self):
        node_fw = Node(state=self.problem.initial_state, parent=None, action=None, cost=0, depth=0)
        node_bw = Node(state=self.problem.goal_state, parent=None, action=None, cost=0, depth=0)

        while True:
            next_nodes_fw = [node_fw.expand(state=s, action=a, cost=1) for s, a in
                             self.problem.successors(node_fw.state)]
            next_nodes_bw = [node_bw.expand(state=s, action=a, cost=1) for s, a in
                             self.problem.successors(node_bw.state)]

            self.fringe_fw = self.strategy_fw.select(new_nodes=next_nodes_fw, fringe=self.fringe_fw)
            self.fringe_bw = self.strategy_bw.select(new_nodes=next_nodes_bw, fringe=self.fringe_bw)

            node_fw = self.fringe_fw.pop()
            node_bw = self.fringe_bw.pop()

            if tuple(node_fw.state.flatten()) not in self.reached_fw.keys():
                self.reached_fw[tuple(node_fw.state.flatten())] = node_fw

            if tuple(node_bw.state.flatten()) not in self.reached_bw.keys():
                self.reached_bw[tuple(node_bw.state.flatten())] = node_bw

            if set.intersection(set(self.reached_fw.keys()), set(self.reached_bw.keys())):
                key = list(set.intersection(set(self.reached_fw.keys()), set(self.reached_bw.keys())))[0]
                return self.join(self.reached_fw[key], self.reached_bw[key])
            self.strategy_fw.add_visited(node_fw.state)
            self.strategy_bw.add_visited(node_bw.state)


class RecursiveBestSearch:
    # INCOMPLETA
    def __init__(self, problem, strategy):
        self.strategy = strategy  # Da passare inesplosa
        self.problem = problem
        self.fringe = []
        self.best_next_node = {}

    def f_value(self, node):
        return node.cost + self.problem.h(node.state)

    def run(self, state, best_next_node=None):
        node = (Node(state=state, depth=0, cost=0, parent=None, action=None))
        next_nodes = [node.expand(state=s, action=a, cost=1) for s, a in self.problem.successors(node.state)]
        sorted_nodes = sorted(next_nodes, key=lambda n: self.f_value(node))
