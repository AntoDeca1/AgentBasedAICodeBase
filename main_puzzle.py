from EightPuzzle.strategy import *
from EightPuzzle.search import ThreeSearch, IterativeDeepiningSearch, BidirectionalSearch, IterativeDeepiningAStar
from EightPuzzle.problem import EightPuzzle
import numpy as np

# TODO:Define intial state and goal state
initial_state = np.array([[1, 2, 3], [8, None, 4], [7, 6, 5]])
final_state = np.array([[2, 8, 1], [None, 4, 3], [7, 6, 5]])
# TODO:Define the problem
problem = EightPuzzle(initial_state=initial_state, goal_state=final_state)
# TODO:Define the strategy
strategy = AStar(problem=problem)
# TODO:Define the search
# search = ThreeSearch(problem=problem, strategy=strategy)
search = BidirectionalSearch(problem=problem, strategy_fw=GraphBreadthFirst(), strategy_bw=GraphBreadthFirst())
# search = IterativeDeepiningSearch(problem=problem)
# search = IterativeDeepiningAStar(problem=problem)
# TODO:Run the search
path = search.run()
print(f"-----Sequence of action to be performed------\n{path}")

# TODO:Sanity check(We check that the founded sequence of action bring to the correct final state)
print("SANITY CHECK")
print("-------Initial-State--------")
print(initial_state)
result = initial_state
i = 1
for action in path:
    result = action(result)
    print(f"------Result------\n{result} \n---action {i}--")
    if (result == final_state).all():
        print("\n------GOAL-STATE-REACHED---- :)")
    i += 1
