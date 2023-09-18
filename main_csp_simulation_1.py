from CSP.problem import CSP
from CSP.backtracking import *
from CSP.constraints import *
from input.words import words

# IN QUESTO CASO E'PRESENTE LA PAROLA ALBERTO NEL CRUCIVERBA
variables = ["W1", "W2"]
domains = {"W1": [word for word in words if len(word) == 6],
           "W2": [word for word in words if len(word) == 3]}


class LetterConstraint(UnaryConstraint):

    def __init__(self, variable, letter, position):
        super(LetterConstraint, self).__init__(variable)
        self.letter = letter
        self.position = position

    def check(self, state):
        if self.variable in state:
            return state[self.variable][self.position] == self.letter
        return True


constraints = [LetterConstraint("W1", letter="l", position=4),
               LetterConstraint("W2", letter="t", position=0)]

problem = CSP(variables=variables,
              domains=domains,
              constraints=constraints)

strategy = BackTracking(problem=problem, var_criterion=degree_heuristic, value_criterion=least_constraining_value)
print(strategy.run({}))
