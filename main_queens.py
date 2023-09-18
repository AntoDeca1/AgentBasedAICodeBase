from NQueens.local_search import HillClimbing, SimulatedAnnealing, GeneticAlghoritm, LocalBeamSearch
from NQueens.problem import NQueensProblem

problem = NQueensProblem(n=8)
# strategy = HillClimbing(problem=problem)
# strategy = SimulatedAnnealing(problem=problem)
strategy = LocalBeamSearch(problem=problem, k=2)
# strategy = GeneticAlghoritm(problem=problem)
print(problem.value(problem.initial_state))
state, conflicts = strategy.run()
print(state,conflicts)
