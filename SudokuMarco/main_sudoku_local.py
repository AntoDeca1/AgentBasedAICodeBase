from src.local_search import HillClimbing,SimulatedAnnealing,Genetic
from src.local_problem import Sudoku_local

# initialize the problem
problem = Sudoku_local()
# choose a strategy
strategy = HillClimbing(problem)
# strategy = SimulatedAnnealing(problem)
# strategy = Genetic(problem)

# run the search
result,state = strategy.run()

print(result)
print(state)
print(f'with a number of conflicts of {problem.conflicts(state)}')

