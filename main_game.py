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
