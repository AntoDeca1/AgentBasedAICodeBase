import numpy as np


class AlphaBeta:
    def __init__(self, game):
        self.game = game

    def max_value(self, state, alpha, beta):
        best_value = -np.inf
        response, _ = self.game.terminal_test(state)
        if response:
            return self.game.player_utility(state)
        next_states = self.game.successors(state)
        for s in next_states:
            value = self.min_value(s, alpha, beta)
            best_value = max(value, best_value)
            if best_value >= beta:
                return best_value
            alpha = max(best_value, alpha)
        return best_value

    def min_value(self, state, alpha, beta):
        best_value = np.inf
        response, _ = self.game.terminal_test(state)
        if response:
            return self.game.player_utility(state)
        next_states = self.game.successors(state)
        for s in next_states:
            value = self.max_value(s, alpha, beta)
            best_value = min(value, best_value)
            if best_value <= alpha:
                return best_value
            beta = min(best_value, beta)
        return best_value

    def best_move(self, state):
        actions = self.game.actions(state)
        best_move = max(actions, key=lambda action: self.min_value(self.game.result(state, action), -np.inf, np.inf))
        return best_move
