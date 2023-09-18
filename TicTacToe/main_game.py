from TicTacToe.game import TicTacToe
from TicTacToe.minimax import MiniMax
from TicTacToe.random_p import Random
from TicTacToe.alphabeta import AlphaBeta

# TODO:Define the game
game = TicTacToe()
# TODO:Define two players
player_1 = AlphaBeta(game=game)
player_2 = AlphaBeta(game=game)
# TODO:In case you want MAX to win a bit select random as second player
#player_2 = Random(game=game)
# TODO:Start the game
moves = game.play(player_1, player_2)
print(moves)
