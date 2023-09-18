from NQueensCSP.contraints import *
from NQueensCSP.csp import CSP
from NQueensCSP.backtracking import *

variables = ["Q0", "Q1", "Q2", "Q3"]
domains = {var: list(range(4)) for var in variables}

# TODO:Per lanciare Ac-3 è necessario mettere i vincoli due volte.(In entrambe le direzioni)
constraints = [QueensConstraints(["Q0", "Q1"]),
               QueensConstraints(["Q1", "Q0"]),
               QueensConstraints(["Q0", "Q2"]),
               QueensConstraints(["Q2", "Q0"]),
               QueensConstraints(["Q0", "Q3"]),
               QueensConstraints(["Q3", "Q0"]),
               QueensConstraints(["Q1", "Q2"]),
               QueensConstraints(["Q2", "Q1"]),
               QueensConstraints(["Q1", "Q3"]),
               QueensConstraints(["Q3", "Q1"]),
               QueensConstraints(["Q2", "Q3"]),
               QueensConstraints(["Q3", "Q2"])]

csp = CSP(variables=variables, domains=domains, constraints=constraints)
strategy = BackTracking(problem=csp, var_criterion=minimum_remaining_values, value_criterion=least_constraining_value)

print(strategy.run_with_forward_checking({}, domains=csp.domains))
