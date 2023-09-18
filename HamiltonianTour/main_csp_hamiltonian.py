from constraints import *
from HamiltonianTour.csp import *
from HamiltonianTour.backtracking import *

# Per capire il problema vedere nella cartella il disegno di riferimento
variables = ["BA", "TA", "SS", "LE", "CR", "TR"]


class AllDiff(Constraint):
    """
    We need that every variable is visited only once
    So this means that the same variable can't have the same number
    """

    def check(self, state):
        variables_in_state = [var for var in self.variables if var in state]
        if variables_in_state is None:
            return True
        values = [state[var] for var in variables_in_state]
        return len(values) == len(set(values))


class NeighbourConstraint(Constraint):
    """
    The cities that are not connected can't have adiacent value
    """

    def check(self, state):
        var_1, var_2 = self.variables
        if var_1 not in state or var_2 not in state:
            return True
        if state[var_1] == (state[var_2] + 1):
            return False
        if (state[var_1] == state[var_2] - 1):
            return False
        return True


domains = {var: list(range(0, 6)) for var in variables}
constraints = [AllDiff(variables),
               NeighbourConstraint(["BA", "SS"]),
               NeighbourConstraint(["BA", "LE"]),
               NeighbourConstraint(["TA", "CR"]),
               NeighbourConstraint(["CR", "SS"]),
               NeighbourConstraint(["TR", "SS"])]

problem = CSP(variables=variables, domains=domains, constraints=constraints)
strategy = BackTracking(problem, var_criterion=degree_heuristic, value_criterion=least_constraining_value)
print(strategy.run_with_forward_checking({}, domains=domains))
