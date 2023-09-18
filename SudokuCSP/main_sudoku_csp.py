from SudokuCSP.contraints import *
from SudokuCSP.utils import *
from SudokuCSP.csp import CSP
from SudokuCSP.backtracking import *

# TODO:The code below could be improved in a way we do not need to manually define all the constraints for row and columns
N = 2
letters = ["A", "B", "C", "D"]
variables = [letter + str(j) for letter in letters for j in range(1, N ** 2 + 1)]
domains = {var: list(range(1, 5)) for var in variables}

# TODO:We define the variables already fixed in the sudoku
variables_to_fix = [("A3", 4),
                    ("C1", 1),
                    ("D1", 4), ("D2", 2), ("D4", 3)]
# TODO:Remove the fixed variable in the domain
domain = domains_filter(domains=domains, variables_to_fix=variables_to_fix)
# TODO:Put the fixed variable in the state
initial_state = state_filter(state={}, variables_to_fix=variables_to_fix)
# TODO:Print the starting condition of the problem
print("VARIABLES", variables)
print("INITIAL-DOMAINS", domain)
print("INITIAL-STATE", initial_state)


# TODO:AllDiff constraint
class AllDiff(Constraint):
    def check(self, state):
        variables_in_the_state = [var for var in self.variables if var in state]
        if len(variables_in_the_state) == 0:
            return True
        values = [state[var] for var in variables_in_the_state]
        return len(values) == len(set(values))


# TODO:Let's create the list of all the constraints in our problem
constraints_on_square = [AllDiff([var for var in variables if var[0] == letter]) for letter in letters]
# TODO:Constraints on rows
constraint_on_row_1 = AllDiff(['A1', 'A2', 'B1', 'B2'])
constraint_on_row_2 = AllDiff(['A3', 'A4', 'B3', 'B4'])
constraint_on_row_3 = AllDiff(['C1', 'C2', 'D1', 'D2'])
constraint_on_row_4 = AllDiff(['C3', 'C4', 'D3', 'D4'])
constraint_on_rows = [constraint_on_row_1, constraint_on_row_2, constraint_on_row_3, constraint_on_row_4]
# TODO:Constraints on columns
constraint_on_col_1 = AllDiff(['A1', 'A3', 'C1', 'C3'])
constraint_on_col_2 = AllDiff(['A2', 'A4', 'C2', 'C4'])
constraint_on_col_3 = AllDiff(['B1', 'B3', 'D1', 'D3'])
constraint_on_col_4 = AllDiff(['B2', 'B4', 'D2', 'D4'])
constraint_on_cols = [constraint_on_col_1, constraint_on_col_2, constraint_on_col_3, constraint_on_col_4]
# TODO:All the constraints in a single list
constraints = constraints_on_square + constraint_on_rows + constraint_on_cols
# TODO:Defining the problem
problem = CSP(variables=variables, domains=domains, constraints=constraints)
# TODO:Defining the strategy
strategy = BackTracking(problem=problem, var_criterion=degree_heuristic, value_criterion=least_constraining_value)
print("------SOLUTION------\n", strategy.run_with_forward_checking(state=initial_state, domains=domains))
# THE SOLUTION IS CORRECT IF YOU CHECK ON THE PDF :)
