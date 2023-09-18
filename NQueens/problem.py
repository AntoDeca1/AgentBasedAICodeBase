import numpy as np


class NQueensProblem:

    def __init__(self, initial_state=None, n=4):
        self.n = n
        if initial_state == None:
            self.initial_state = self.random_state()
        else:
            self.initial_state = initial_state
        self.max_conflits = np.sum([i for i in range(0, n)])

    def successors(self, state):
        actions = self.actions(state)
        new_states = [self.result(state, action) for action in actions]
        return new_states

    def random_state(self):
        rand_state = [np.random.randint(0, self.n) for _ in range(self.n)]
        return rand_state

    def actions(self, state):
        actions = []
        range = list(np.arange(self.n))
        for idx, el in enumerate(state):
            temp = range.copy()
            temp.remove(el)
            new_actions = [(idx, value) for value in temp]
            actions.extend(new_actions)
        return actions

    def goal_test(self, state):
        return self.conflicts(state) == 0

    def result(self, state, action):
        col, value = action
        temp = list(state).copy()
        temp[col] = value
        return tuple(temp)

    # def conflicts(self, state):
    #     conflicts_counter = 0
    #     row_col = list(self.row_and_col(state))
    #     temp = row_col.copy()
    #     for current_row, current_col in row_col:
    #         temp.pop(0)
    #         for row, col in temp:
    #             if (current_col + current_row) == (row + col):
    #                 conflicts_counter += 1
    #             if current_row == row:
    #                 conflicts_counter += 1
    #             if abs(current_col - current_row) == abs(row - col):
    #                 conflicts_counter += 1
    #     return conflicts_counter

    def conflicts(self, state):
        conflicts = 0
        for queen, row in enumerate(state):
            for i in range(queen + 1, self.n):
                if state[i] == row:
                    conflicts += 1
                if (state[i] + i) == (row + queen) or abs(state[i] - i) == abs(row - queen):
                    conflicts += 1
        return conflicts

    def row_and_col(self, state):
        return [(el, idx) for idx, el in enumerate(state)]

    def value(self, state):
        return self.max_conflits - self.conflicts(state)
