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





