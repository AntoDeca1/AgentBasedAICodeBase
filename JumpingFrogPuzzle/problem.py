import numpy as np


class JumpingFrog:
    def __init__(self, N=2):
        self.N = N
        self.initial_state = self.initialize_state()
        self.goal_state = self.initial_state[::-1]
        print()

    def initialize_state(self):
        """
        Utility function to create the initial state
        :return:
        """
        left_frogs = ["L" for _ in range(self.N)]
        right_frogs = ["R" for _ in range(self.N)]
        final_state = left_frogs + ["."] + right_frogs
        return final_state

    def successors(self, state):
        actions = self.actions(state)
        return [(self.result(state, action), action) for action in actions]

    def actions(self, state):
        """
        Depending on the type of frog and the depending on the position of the frog we are able to do different actions
        RULES:
        A left frog can shift 1 place to the blank 1 in the right direction but also 2 places if there is a right frog after
        EXAMPLE:
        ["L","L",".","R","R"]
        Only the second left frog can move right to .
        Only the second right frog can move left to .
        actions=[(1,2),(3,2)]
        :param state:
        :return:
        """
        blank_position = state.index(".")
        actions = []
        for idx, el in enumerate(state):
            if el == "L" and blank_position - idx == 1:
                actions.append((idx, blank_position))
            if el == "L" and blank_position - idx == 2 and state[idx + 1] == "R":
                actions.append((idx, blank_position))
            if el == "R" and idx - blank_position == 1:
                actions.append((idx, blank_position))
            if el == "R" and idx - blank_position == 2 and state[idx - 1] == "L":
                actions.append((idx, blank_position))
        return actions

    def result(self, state, action):
        element_index, blank_index = action
        new_state = state.copy()
        temp = new_state[element_index]
        new_state[element_index] = "."
        new_state[blank_index] = temp
        return new_state

    def h(self, state):
        """
        The idea behind this heuristic is to count the number of frogs that are on the opposite side
        Example:
        We know that in the case of N=2:
        initial_state=["L","L",".","R","R"]
        goal_state=["R","R",".","L","L"]
        So we count +=1 if a Left Frog is on the right side and also when a Right frog is on the left side
        The heuristic needs to be 0 in the goal state and so i substract the computed value from the number of frog
        :param state:
        :return:
        """
        good = 0
        for idx, el in enumerate(state):
            if el == "L" and idx > (len(state) / 2):
                good += 1
            if el == "R" and idx < (len(state) / 2):
                good += 1
        return (self.N * 2) - good

    def goal_test(self, state):
        return state == self.goal_state


problem = JumpingFrog()
problem.successors(["L", ".", "L", "R", "R"])
