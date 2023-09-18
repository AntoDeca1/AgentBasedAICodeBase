from WaterPooring.problem import WaterPouring
from WaterPooring.node import Node
from WaterPooring.strategy import *
from WaterPooring.search import *

# TODO:Define the initial configuration of the problem
initial_state = (0, 0)
goal_state = 4
capacities = (5, 3)
# TODO:Create an instance of the problem
problem = WaterPouring(initial_state=initial_state, capacities=capacities, goal=4)
# TODO:Define the possible strategy
strategy_1 = AStar(problem=problem)
strategy_2 = GraphBreadthFirst()
strategy_3 = GraphDepthFirst()
# TODO:Define the type of search
search = TreeSearch(problem=problem, strategy=strategy_1)
# TODO:Run the search and get the results
message, node, actions = search.run()
print("FinalNode", node)
print("Number of actions", len(actions))
# TODO:Check that the resulting actions bring to the state
print("---------CHECK------------")
print(f"Initial_state -->{initial_state}")
state = tuple(initial_state)
for action in actions:
    move, i, j = action
    state = move(state, i, j)
    print(f"NextState\n{state}")
