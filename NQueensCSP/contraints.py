class Constraint:
    def __init__(self, variables):
        self.variables = variables
        self.degree = len(variables)

    def check(self, state):
        return True

    def arc(self):
        arc = None
        if self.degree == 2:
            arc = tuple(self.variables)
        return arc

    def neighbours(self, var):
        if var in self.variables:
            neighbours = list(self.variables)
            neighbours.remove(var)
            return neighbours


class UnaryConstraint(Constraint):
    def __init__(self, variable):
        self.variable = variable
        super(UnaryConstraint, self).__init__(variables=variable)

    def check(self, state):
        return True


class ValueConstraint(UnaryConstraint):
    def __init__(self, variable, accepted_values):
        super(ValueConstraint, self).__init__(variable)
        self.accepted_values = accepted_values

    def check(self, state):
        if self.variable in state:
            return state[self.variable] in self.accepted_values
        return True


class DifferentValues(Constraint):
    def check(self, state):
        values = [state[var] for var in self.variables if var in state]
        return len(values) == len(set(values))


# The specific constraint needed for this problem
class QueensConstraints(Constraint):
    def check(self, state):

        columns = {"Q0": 0, "Q1": 1, "Q2": 2, "Q3": 3}
        for variable in self.variables:
            if variable not in state:
                return True
        variable_1, variable_2 = self.variables
        if state[variable_1] == state[variable_2] or (
                abs(state[variable_1] - columns[variable_1]) == abs(state[variable_2] - columns[variable_2])):
            return False
        return True
