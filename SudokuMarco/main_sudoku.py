# sudoku can be modeled as a csp (2by2 sudoku)
from src.problem import CSP
from src.constraints import Constraint, DifferentValues
from src.backtracking import BackTracking, minimum_remaining_values, least_constraining_value

variables = ['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4','D1','D2','D3','D4']
domains ={}
for var in variables:
    domains[var] = [1,2,3,4]

class DifferentNumbers(Constraint):
    def __init__(self,variables):
        super(DifferentNumbers, self).__init__(variables)
    def check(self, state):
        values = [state[var] for var in self.variables if var in state]
        return len(values) == len(set(values))

constraints=[
    # different on the same row
    DifferentNumbers(['A1','A2']),
    DifferentNumbers(['A1','A3']),
    DifferentNumbers(['A1','A4']),
    DifferentNumbers(['A2','A3']),
    DifferentNumbers(['A2', 'A4']),
    DifferentNumbers(['A3','A4']),
    # different on the same column
    DifferentNumbers(['A1','B1']),
    DifferentNumbers(['A1', 'C1']),
    DifferentNumbers(['A1', 'D1']),
    DifferentNumbers(['B1', 'C1']),
    DifferentNumbers(['B1', 'D1']),
    DifferentNumbers(['C1', 'D1']),
    # different in the same cell
    DifferentNumbers(['A1','B2']),
    # different on the same row
    DifferentNumbers(['B1', 'B2']),
    DifferentNumbers(['B1', 'B3']),
    DifferentNumbers(['B1', 'B4']),
    DifferentNumbers(['B2', 'B3']),
    DifferentNumbers(['B2', 'B4']),
    DifferentNumbers(['B3', 'B4']),
    # different on the same column
    DifferentNumbers(['A2', 'B2']),
    DifferentNumbers(['A2', 'C2']),
    DifferentNumbers(['A2', 'D2']),
    DifferentNumbers(['B2', 'C2']),
    DifferentNumbers(['B2', 'D2']),
    DifferentNumbers(['C2', 'D2']),
    # different in the same cell
    DifferentNumbers(['A3', 'B4']),
    # different on the same row
    DifferentNumbers(['C1', 'C2']),
    DifferentNumbers(['C1', 'C3']),
    DifferentNumbers(['C1', 'C4']),
    DifferentNumbers(['C2', 'C3']),
    DifferentNumbers(['C2', 'C4']),
    DifferentNumbers(['C3', 'C4']),
    # different on the same column
    DifferentNumbers(['A3', 'B3']),
    DifferentNumbers(['A3', 'C3']),
    DifferentNumbers(['A3', 'D3']),
    DifferentNumbers(['B3', 'C3']),
    DifferentNumbers(['B3', 'D3']),
    DifferentNumbers(['C3', 'D3']),
    # different in the same cell
    DifferentNumbers(['C1', 'D2']),
    # different on the same row
    DifferentNumbers(['D1', 'D2']),
    DifferentNumbers(['D1', 'D3']),
    DifferentNumbers(['D1', 'D4']),
    DifferentNumbers(['D2', 'D3']),
    DifferentNumbers(['D2', 'D4']),
    DifferentNumbers(['D3', 'D4']),
    # different on the same column
    DifferentNumbers(['A4', 'B4']),
    DifferentNumbers(['A4', 'C4']),
    DifferentNumbers(['A4', 'D4']),
    DifferentNumbers(['B4', 'C4']),
    DifferentNumbers(['B4', 'D4']),
    DifferentNumbers(['C4', 'D4']),
    # different in the same cell
    DifferentNumbers(['C3', 'D4'])
]

csp = CSP(variables,domains,constraints)
search = BackTracking(csp,var_criterion=minimum_remaining_values,value_criterion=least_constraining_value)
initial_state = {}
result = search.run_with_forward_checking(initial_state,csp.domains)
print(result)