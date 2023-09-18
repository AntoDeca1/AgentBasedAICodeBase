from input.words import words
from CSP.constraints import *
from CSP.problem import CSP
from CSP.backtracking import *
from CSP.ac3 import AC3

variables = ["W1", "W2", "W3"]

domains = {"W1": [word for word in words if len(word) == 6],
           "W2": [word for word in words if len(word) == 7],
           "W3": [word for word in words if len(word) == 3]}


class LetterConstraint(Constraint):

    def __init__(self, variables, positions):
        super(LetterConstraint, self).__init__(variables=variables)
        self.positions = positions

    def check(self, state):
        variable_1, variable_2 = self.variables
        position_1, position_2 = self.positions
        if variable_1 in state and variable_2 in state:
            return state[variable_1][position_1] == state[variable_2][position_2]
        return True


constraints = [LetterConstraint(["W1", "W2"], [4, 1]),
               LetterConstraint(["W2", "W1"], [1, 4]),
               LetterConstraint(["W2", "W3"], [5, 0]),
               LetterConstraint(["W3", "W2"], [0, 5])]

problem = CSP(variables=variables, domains=domains, constraints=constraints)


strategy = BackTracking(problem=problem, var_criterion=minimum_remaining_values, value_criterion=random_assignment)
print(strategy.run_with_forward_checking({}, domains=problem.domains))
