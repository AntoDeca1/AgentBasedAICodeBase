from CSP.constraints import *
from CSP.backtracking import *
from CSP.problem import CSP

variables = ["C1", "C2", "C3", "C4", "C5"]

# TODO:Instead of defining unary constraint like C1!=3.. we restrict the domain of the variabile

domains = {"C1": ["A", "C"], "C2": ["A"], "C3": ["B", "C"], "C4": ["B", "C"], "C5": ["A", "B"]}


# TODO:Solo per ripetizione lo riscriviamo,potremmo usare differentValues presente nel file CSP.constraints
class DifferentConstraint(Constraint):

    def __init__(self, variables):
        super(DifferentConstraint,self).__init__(variables=variables)

    def check(self, state):
        values = [state[var] for var in self.variables if var in state]
        return len(values) == len(set(values))


constraints = [DifferentConstraint(["C1", "C2"]),
               DifferentConstraint(["C2", "C3"]),
               DifferentConstraint(["C2", "C4"]),
               DifferentConstraint(["C3", "C4"])]

problem = CSP(variables=variables, domains=domains, constraints=constraints)
strategy = BackTracking(problem=problem, var_criterion=minimum_remaining_values,
                        value_criterion=least_constraining_value)

print("-------SCHEDULE----------")
print(strategy.run_with_forward_checking({}, domains=problem.domains))
