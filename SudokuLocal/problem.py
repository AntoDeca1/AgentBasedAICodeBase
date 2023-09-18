import numpy as np
from collections import Counter
from SudokuLocal.local_search import *


# MIGLIORABILE :(
class SudokuLocal:
    def __init__(self, initial_state=None, N=4):
        self.N = N
        self.initial_state = initial_state
        self.max_conflicts = 36
        if self.initial_state is None:
            self.initial_state = np.array([[None, None, None, None],
                                           [4, None, None, None, ],
                                           [1, None, 4, 2],
                                           [None, None, None, 3]])

    def successors(self, state):
        actions = self.actions(state)
        return [self.result(state, action) for action in actions]

    def actions(self, state):
        possible_values = list(range(1, self.N + 1))
        actions = []
        for i in range(self.N):
            for j in range(self.N):
                if state[i, j] == None:
                    for value in possible_values:
                        actions.append(((i, j), value))
        np.random.shuffle(actions)
        return actions

    def result(self, state, action):
        position, value = action
        new_state = state.copy()
        new_state[position] = value
        return new_state

    def conflicts(self, state):
        conflicts = 0

        first_square = state[:2, :2].flatten()
        second_square = state[:2, 2:].flatten()
        third_square = state[2:, :2].flatten()
        fourth_square = state[2:, 2:].flatten()
        squares = [first_square, second_square, third_square, fourth_square]
        for square in squares:
            counter = Counter(square)
            for k, v in counter.items():
                if v >= 2 and k != None:
                    conflicts += v - 1
        for i in range(self.N):
            row_i = state[i, :].flatten()
            col_i = state[:, i].flatten()
            counter_row = Counter(row_i)
            counter_col = Counter(col_i)
            for k, v in counter_row.items():
                if v >= 2 and k != None:
                    conflicts += v - 1
            for k, v in counter_col.items():
                if v >= 2 and k != None:
                    conflicts += v - 1
        return conflicts

    def value(self, state):
        return self.max_conflicts - self.conflicts(state) - list(state.flatten()).count(None)


problem = SudokuLocal()
strategy = HillClimbing(problem=problem)
print(strategy.run())
