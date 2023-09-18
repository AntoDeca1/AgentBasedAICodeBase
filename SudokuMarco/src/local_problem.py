from copy import deepcopy

class Sudoku_local:
    def __init__(self, initial_state=None):
        if initial_state is None:
            initial_state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.initial_state = initial_state
        self.max_conflicts = 5 * 16

    def successors(self, state):
        possible_actions = self.actions(state)
        return [(self.result(state,action),action) for action in possible_actions]

    def actions(self, state):
        actions =[] # list of assignable values (from 1 to 4) in the empty spots
        empty = self.get_blank_spots(state)
        for spot in empty:
            for i in range(5):
                new_spot = list(spot)
                new_spot.append(i)
                actions.append(new_spot)
        return actions

    def result(self, state, action):
        row,col,value = action
        new_state = deepcopy(state)
        new_state[row][col] = value
        return new_state

    def conflicts(self, state):
        conflicts = 0
        # check the conflicts on the rows
        for row in range(4):
            for col in range(4):
                for col1 in range(col + 1, 4):
                    if state[row][col] == state[row][col1]:
                        conflicts += 1
        # check the conflicts on the columns
        for col in range(4):
            for row in range(4):
                for row1 in range(row + 1, 4):
                    if state[row][col] == state[row1][col]:
                        conflicts += 1
        # check the conflicts in the same square
        if state[0][0] == state[1][1]:
            conflicts += 1
        if state[0][1] == state[1][0]:
            conflicts += 1
        if state[2][2] == state[3][3]:
            conflicts += 1
        if state[2][3] == state[3][2]:
            conflicts += 1
        if state[0][2] == state[1][3]:
            conflicts += 1
        if state[0][3] == state[1][2]:
            conflicts += 1
        if state[2][0] == state[3][1]:
            conflicts += 1
        if state[3][0] == state[2][1]:
            conflicts += 1
        return conflicts

    def value(self, state):
        return self.count_non_zero(state) - self.conflicts(state)

    def count_non_zero(self, state):
        count = 0
        for a in state:
            for b in a:
                if b == 0:
                    count += 1
        return count

    def get_blank_spots(self, state):
        blank_spots = []
        for row in range(4):
            for col in range(4):
                if state[row][col] == 0:
                    blank_spots.append((row, col))
        return blank_spots

    def goal_test(self, state):
        return self.count_non_zero(state) == 0
