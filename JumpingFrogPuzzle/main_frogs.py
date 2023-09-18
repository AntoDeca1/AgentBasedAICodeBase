from JumpingFrogPuzzle.strategy import *
from JumpingFrogPuzzle.problem import JumpingFrog
from JumpingFrogPuzzle.search import *

problem = JumpingFrog(N=3)
strategy_1 = GraphDepthFirst()
strategy_2 = AStar(problem=problem)
# search = ThreeSearch(problem=problem, strategy=strategy_1)
search = IterativeDeepeningSearch(problem=problem)


actions = search.run()

print("-------------ACTIONS-----------------")
print(actions)

state = problem.initial_state
print("----------INITIAL-STATE-------")
print(state)
print("-----------ACTIONS-CHECK--------")
for action in actions:
    state = problem.result(state, action)
    print(f"We moved to {state} with the action {action}")
