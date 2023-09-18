from CSP.problem import *
from CSP.backtracking import *
from CSP.constraints import Constraint

problem = MapColoring
search = BackTracking(problem=problem, var_criterion=degree_heuristic, value_criterion=least_constraining_value)
initial_state={

}

print(search.run_with_forward_checking(initial_state, problem.domains))

