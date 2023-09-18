import random
from crossword_local_example.local_search import *

from input.words import words


class Problem:

    def __init__(self, initial_state=None):
        self.initial_state = initial_state
        if self.initial_state == None:
            self.initial_state = []

    def actions(self, state):
        """
        action_1:Inserire una parola randomica di lunghezza 6
        action_2:Inserire una parola randomica di lunghezza 7
        action_3:Inserire una parola randomica di lunghezza 3
        :param state:
        :return:the possible actions
        """
        action_1 = random.choice([word for word in words if len(word) == 6])
        action_2 = random.choice([word for word in words if len(word) == 7])
        action_3 = random.choice([word for word in words if len(word) == 3])
        return [action_1, action_2, action_3]

    def result(self, state, action):
        if len(action) == 6:
            if len(state) >= 1:
                new_state = state.copy()
                new_state[0] = action
            else:
                new_state = state.copy() + [action, ]
            return new_state
        if len(action) == 7:
            if len(state) >= 2:
                new_state = state.copy()
                new_state[1] = action
            else:
                new_state = state.copy() + [action, ]
            return new_state
        if len(action) == 3:
            if len(state) >= 3:
                new_state = state.copy()
                new_state[2] = action
            else:
                new_state = state.copy() + [action, ]
            return new_state
        raise ValueError

    def successors(self, state):
        actions = self.actions(state)
        return [self.result(state, action) for action in actions]

    def utility(self, state):
        utility = 0
        utility = utility + len(state)
        if len(state) >= 2:
            if state[0][4] != state[1][1]:
                utility = utility - 0.3
        if len(state) >= 3:
            if state[1][5] != state[2][0]:
                utility = utility - 0.3
        return utility


problem = Problem()
print(problem.actions(()))
print(problem.utility(('sicure', 'appostò', 'amò')))
#strategy = HillClimbing(problem=problem)
strategy = SimulatedAnnealing(problem=problem)
print(strategy.run())
