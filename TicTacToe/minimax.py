import numpy as np


class MiniMax:
    def __init__(self, game):
        self.game = game

    def max_value(self, state):
        response, _ = self.game.terminal_test(state)
        if response == True:
            return self.game.player_utility(state)
        values = [self.min_value(state) for state in self.game.successors(state)]
        return max(values)

    def min_value(self, state):
        response, _ = self.game.terminal_test(state)
        if response == True:
            return self.game.player_utility(state)
        values = [self.max_value(state) for state in self.game.successors(state)]
        return min(values)

    def best_move(self, state):
        actions = self.game.actions(state)
        best_move = max(actions, key=lambda action: self.min_value(self.game.result(state, action)))
        return best_move



