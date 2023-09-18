import numpy as np

"""
N.B:L'idea fondamentale che non viene in mente subito è quella di essere certi che duranti il MINMAX non venga inserito sempre lo stesso simbolo
Inizialmente infatti quando valutavo i successors non codificavo l'informazione del corrente simbolo e di conseguenza mettevo sempre la X
L'idea è stata pensare al fatto che il simbolo che dobbiamo mettere sulla board dipende da quanti simboli ci sono attualmente sulla board,se sono pari allora
il prossimo sarà X,al contrario O.
"""


class TicTacToe:
    def __init__(self, current_player="MAX"):
        self.current_player = current_player
        self.initial_state = (np.full((3, 3), None))

    def successors(self, state):
        """
        Return all the possible state starting from the current state
        :param state:
        :return:
        """
        actions = self.actions(state)
        new_states = [self.result(state, action) for action in actions]
        return new_states

    def actions(self, state):
        """
        Return all the possible actions that could be made starting from the current state
        :param state:
        :return:
        """
        actions = []
        symbol = self.current_symbol(state)
        for i in range(3):
            for j in range(3):
                if state[i, j] == None:
                    actions.append(((i, j), symbol))
        np.random.shuffle(actions)
        return actions

    def result(self, state, action):
        """
        Return the state reachable by performing the given action on the given state
        :param state:
        :return:
        """
        action, symbol = action
        temp = state.copy()
        temp[action] = symbol
        return temp

    def terminal_test(self, state):
        """
        Checks if the current state is a terminal one
        1)If there no blank tiles aviable
        2)If there are tree Cross on row/column
        3)If there are tree Circles on row/column
        4)If there are tree Circles/Cross on one of the two diagonals
        :param state:
        :return:
        """

        first_diag = list(np.diag(state))
        second_diag = list(np.diag(np.fliplr(state)))
        if first_diag.count("X") == 3: return True, "X"
        if first_diag.count("O") == 3: return True, "O"
        if second_diag.count("X") == 3: return True, "X"
        if second_diag.count("O") == 3: return True, "O"

        for i in range(3):
            row = list(state[i, :])
            col = list(state[:, i])
            if row.count("X") == 3: return True, "X"
            if col.count("X") == 3: return True, "X"
            if row.count("O") == 3: return True, "O"
            if col.count("O") == 3: return True, "O"
        if list(state.flatten()).count(None) == 0:
            return True, "Draw"

        return False, "BOH"

    def current_symbol(self, state):
        """
        The symbol that needs to be inserted depends on the number of symbols on the board
        X if we have an even number of symbols(X or O)
        O if we have an odd number of symbols(X or O)
        In this way i evoided to bring in the state this information since is encoded in the configuration
        :param state:
        :return:
        """
        flattened_state = list(state.flatten())
        if (flattened_state.count("X") + flattened_state.count("O")) % 2 == 0:
            return "X"
        else:
            return "O"

    def utility(self, state):
        """
        Return the utilty with respect to MAX
        :param state:
        :return:
        """
        response, symbol = self.terminal_test(state)
        if symbol == "X":
            return 1
        if symbol == "O":
            return -1
        return 0

    def next_player(self):
        """
        Change the player.This is useful for two player games
        :return:
        """
        if self.current_player == "MAX":
            self.current_player = "MIN"
        else:
            self.current_player = "MAX"

    def player_utility(self, state):
        """
        Return the utility with respect to the current player
        If the player is MIN we need to invert the sign,in this way the MINMAX will find the best value for min
        """
        if self.current_player == "MAX":
            return self.utility(state)
        else:
            return -self.utility(state)

    def play(self, player_1, player_2):
        """
        Simulate a two game player.The functions change the player at every turn
        :param player_1:
        :param player_2:
        :return:
        """
        moves = []
        state = self.initial_state
        players = [player_1, player_2]
        while True:
            for player in players:
                print(state)
                if self.terminal_test(state)[0]:
                    print(self.utility(state))
                    return moves
                move = player.best_move(state)
                state = self.result(state, move)
                moves.append(move[0])
                self.next_player()
