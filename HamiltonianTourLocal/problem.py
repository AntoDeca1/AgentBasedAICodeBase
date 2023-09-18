from HamiltonianTourLocal.graph import graph
from collections import Counter
from HamiltonianTourLocal.local_search import *


class HamiltonianTour:

    def __init__(self, environment, initial_state={}):
        self.initial_state = initial_state
        self.environment = environment

    def successors(self, state):
        actions = self.actions(state)
        return [self.result(state, action) for action in actions]

    def actions(self, state):
        if len(state) == 0:
            return [(k, 1) for k, v in self.environment.items()]
        else:
            last_city = self.find_last_city(state)
            return [(el, state[last_city] + 1) for el in self.environment[last_city]]

    def result(self, state, action):
        key, val = action
        new_state = dict(state)
        new_state[key] = val
        return new_state

    def value(self, state):
        return (len(state) - self.penalties(state))

    def penalties(self, state):
        penalties = 0
        c = Counter(state.keys())
        for el in c.values():
            if el >= 2:
                penalties += el - 1
        return penalties

    def find_last_city(self, state):
        """
        Return the last city in the path
        :param state:
        :return:
        """
        return max(state, key=lambda x: state[x])


problem = HamiltonianTour(environment=graph)
strategy = HillClimbing(problem=problem)
print(strategy.run())
