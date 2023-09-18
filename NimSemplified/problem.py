import numpy as np
from NimSemplified.minimax import Minimax, Random

"""
Nim is a game that involves removing objects from some number of distinct piles1. Players take turns removing objects, and may remove any number of objects from a single pile on their turn.
The loser is the player that is forced to pick up the last object. The game is typically played with at least three piles,but we will consider a simplified version with only two piles and two objects per pile.
Here is an illustration of one possible game:
  Initial State ->                                     ::
  Andy removes one object from the left ->             .:
  Barb removes one object from the right ->            ..
  Andy removes one object from the left, and wins ->    .
(a) Draw the complete game tree for this game. The value of a loss for Andy is -1, and the value if a win is +1.
(b) Label each node in your game tree with the Minimax value for that node. Would you rather go first or second in this game?
"""

class NimSemplified:
    def __init__(self, initial_state=None, player="MAX"):
        self.initial_state = initial_state
        self.player = player
        if self.initial_state == None:
            self.initial_state = (np.array([['*', '*'], ['*', '*']]), 0)

    def terminal_test(self, state):
        matrix = state[0]
        return list(matrix.flatten()).count("0") == 3

    def utility(self, state):
        if self.terminal_test(state):
            if state[1] % 2 == 0:
                return -1
            else:
                return 1

    def player_utility(self, state):
        utility = self.utility(state)
        if self.player == "MAX":
            return utility
        else:
            return -utility

    def successors(self, state):
        actions = self.actions(state)
        successors = [self.result(state, action) for action in actions]
        return successors

    def result(self, state, action):
        new_state = list(state).copy()
        copy_0 = new_state[0].copy()
        copy_1 = new_state[1] + 1
        if action == 0:
            copy_0[0, 0] = "0"
            copy_0[0, 1] = "0"
        elif action == 1:
            copy_0[1, 0] = "0"
            copy_0[1, 1] = "0"
        else:
            copy_0[tuple(action)] = "0"
        return [copy_0, copy_1]

    def actions(self, state):
        actions = []
        pile_1 = state[0][0, :]
        pile_2 = state[0][1, :]
        for i in range(len(state)):
            for j in range(len(state)):
                if state[0][i, j] != "0":
                    actions.append(([i, j]))
        if list(pile_1).count('*') == 2 and self.count_removed_elements(state) < 2:
            actions.append((0))
        if list(pile_2).count('*') == 2 and self.count_removed_elements(state) < 2:
            actions.append((1))
        return actions

    def count_removed_elements(self, state):
        matrix = state[0]
        flatten_state = matrix.flatten()
        return list(flatten_state).count("0")

    def next_player(self):
        if self.player == "MAX":
            self.player = "MIN"
        else:
            self.player = "MAX"

    def play(self, player_1, player_2):
        actions = []
        state = self.initial_state
        players = [player_1, player_2]
        while True:
            for player in players:
                print(f"{state[0]}\t{self.player}\n ")
                if self.terminal_test(state):
                    return actions
                action = player.best_move(state)
                state = self.result(state, action)
                actions.append(action)
                self.next_player()


problem = NimSemplified()
# strategy = Minimax(game=problem)
player_1 = Random(game=problem)
player_2 = Minimax(game=problem)
print(problem.play(player_1, player_2))
# print(strategy.best_move((np.array([['*', '*'], ['*', '*']]), 0)))
          