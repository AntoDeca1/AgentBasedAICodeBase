import random


class Minimax:
    def __init__(self, game):
        self.game = game

    def max_value(self, state):
        if self.game.terminal_test(state):
            return self.game.player_utility(state)
        values = [self.min_value(s) for s in self.game.successors(state)]
        return max(values)

    def min_value(self, state):
        if self.game.terminal_test(state):
            return self.game.player_utility(state)
        values = [self.max_value(s) for s in self.game.successors(state)]
        return min(values)

    def best_move(self, state):
        actions = self.game.actions(state)
        return max(actions, key=lambda action: self.min_value(self.game.result(state, action)))


class Random:
    def __init__(self, game):
        self.game = game

    def best_move(self, state):
        actions = self.game.actions(state)
        return random.choice(actions)
