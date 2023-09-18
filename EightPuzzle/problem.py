import numpy as np


class EightPuzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def successors(self, state):
        actions = self.actions(state)
        new_states = [(self.result(state, action), action) for action in actions]
        return new_states

    def result(self, state, action):
        return action(state)

    def actions(self, state):
        possible_actions = []
        row_pos, col_pos = self.get_blank_tiles(state)
        if row_pos == 0:
            possible_actions.extend([self._down])
        if row_pos == 1:
            possible_actions.extend([self._down, self._up])
        if row_pos == 2:
            possible_actions.extend([self._up])
        if col_pos == 0:
            possible_actions.extend([self._right])
        if col_pos == 1:
            possible_actions.extend([self._right, self._left])
        if col_pos == 2:
            possible_actions.extend([self._left])
        return possible_actions

    def goal_test(self, state):
        return (state == self.goal_state).all()

    def h(self, state):
        """
        Num of misplaced tiles
        :param state:
        :return:
        """
        correctly_placed = np.sum(state == self.goal_state)
        if self.get_blank_tiles(state) == self.get_blank_tiles(self.goal_state):
            correctly_placed = correctly_placed - 1
        return 8 - correctly_placed

    def _up(self, state):
        blank_row, blank_col = self.get_blank_tiles(state)
        el_row = blank_row - 1
        el_col = blank_col
        blank_position = (blank_row, blank_col)
        new_postion = (el_row, el_col)
        return self.swap(state, blank_position, new_postion)

    def _down(self, state):
        blank_row, blank_col = self.get_blank_tiles(state)
        el_row = blank_row + 1
        el_col = blank_col
        blank_position = (blank_row, blank_col)
        new_postion = (el_row, el_col)
        return self.swap(state, blank_position, new_postion)

    def _right(self, state):
        blank_row, blank_col = self.get_blank_tiles(state)
        el_row = blank_row
        el_col = blank_col + 1
        blank_position = (blank_row, blank_col)
        new_postion = (el_row, el_col)
        return self.swap(state, blank_position, new_postion)

    def _left(self, state):
        blank_row, blank_col = self.get_blank_tiles(state)
        el_row = blank_row
        el_col = blank_col - 1
        blank_position = (blank_row, blank_col)
        new_postion = (el_row, el_col)
        return self.swap(state, blank_position, new_postion)

    @staticmethod
    def get_blank_tiles(state):
        blank_position = np.where(state == None)
        row_pos = blank_position[0][0]
        col_pos = blank_position[1][0]
        position = (row_pos, col_pos)
        return position

    @staticmethod
    def swap(state, blank_position, el_position):
        copy = state.copy()
        temp = copy[el_position]
        copy[el_position] = None
        copy[blank_position] = temp
        return copy

    def reverse_action(self, function):
        """
        Utility function that was used only for implementing the bidirectional search
        N.B:We need this function because the action in this problem strictly depends on the state on witch
        are applied.
        So the function left in the forward fringe is the right function in the backward one
        :return:
        """
        if function == self._right:
            return self._left
        if function == self._left:
            return self._right
        if function == self._up:
            return self._down
        if function == self._down:
            return self._up
