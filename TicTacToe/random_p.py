import numpy as np


class Random:
    def __init__(self, game):
        self.game = game

    def best_move(self, state):
        actions = self.game.actions(state)
        random_index = np.random.randint(0, len(actions))
        return actions[random_index]
