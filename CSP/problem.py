from CSP.constraints import DifferentValues


class CSP:

    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def consistent(self, state):
        return all([c.check(state) for c in self.constraints])

    def complete(self, state):
        return len(self.variables) == len(state)

    def goal_test(self, state):
        if self.consistent(state) and self.complete(state):
            return True
        else:
            return False

    def assign(self, state, variable, value):
        """
        Return a new state where the input variable is assigned to the input value
        :param state:
        :param variable:
        :param value:
        :return:
        """
        if variable in self.variables and value in self.domains[variable]:
            new_state = dict(state)
            new_state[variable] = value
            return new_state
        return ValueError

    def legal_moves(self, state, variable):
        """
        Retrieve the possible legal value given the current state and a input variable
        :param state:
        :param variable:
        :return:
        """
        values = self.domains[variable]
        return [value for value in values if self.consistent(self.assign(state, variable, value))]

    def rollback(self, state, variable):
        """
        Go back to the previous assignment
        :param state:
        :param variable:
        :return:
        """
        if variable in self.variables:
            new_state = dict(state)
            del new_state[variable]
            return new_state
        raise ValueError

    def count_constraints(self, var_1, var_2):
        """
        Count the constraint between the two variables
        :param var_1:
        :param var_2:
        :return:
        """
        return sum([1 for c in self.constraints if var_1 in c.variables and var_2 in c.variables])

    def remaining_constraints(self, state, variable):
        """
        Return the number of constraints between the input variable and the remaining one(not yet assigned)
        :param state:
        :param variable:
        :return:
        """
        remaining_variables = [variable for var in self.variables if var not in state and var != variable]
        if remaining_variables:
            return sum([self.count_constraints(variable, var) for var in remaining_variables])
        else:
            return 0

    def assignable_variables(self, state):
        """
        Return the variables not assigned yet
        :param state:
        :return:
        """
        return [variable for variable in self.variables if variable not in state]

    def remove_inconsistent_values(self, arc, actual_state):
        """
        DA CONTROLLARE
        Given an arc constraint over the variable x_i,x_j check that the values of x_i have at least one value
        in x_j that satisfies the constraint,otherwise remove that value of x_i from its domain
        :param arc: an arc constraint
        :param state: the problem state
        :return: True if some value in x_i domains have been removed,False otherwise
        """
        x_i, x_j = arc.variables

        removed = False

        for value_i in self.domains[x_i]:
            # TODO:All the values in  x_i needs to have at least one value in x_j that satisfy this constraint
            state = self.assign(state=actual_state, variable=x_i, value=value_i)

            # TODO:Iterate on the domains of x_j and sees if value_j satisfy the constraint
            assignments = [arc.check(self.assign(state, variable=x_j, value=value_j)) for value_j in self.domains[x_j]]

            # TODO:For us is sufficient that at least one in x_j satisfy the constraint
            if not any(assignments):
                # If not we have to remove that value in order to enforce the consistency
                self.domains[x_i].remove(value_i)
                print(f"Removing {value_i} from {x_i}")
                removed = True
        return removed


map_vars = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
map_domains = {var: ['green', 'red', 'blue'] for var in map_vars}
map_cons = [DifferentValues(['WA', 'NT']),
            DifferentValues(['NT', 'WA']),
            DifferentValues(['WA', 'SA']),
            DifferentValues(['SA', 'WA']),
            DifferentValues(['SA', 'NT']),
            DifferentValues(['NT', 'SA']),
            DifferentValues(['SA', 'Q']),
            DifferentValues(['Q', 'SA']),
            DifferentValues(['SA', 'NSW']),
            DifferentValues(['NSW', 'SA']),
            DifferentValues(['SA', 'V']),
            DifferentValues(['V', 'SA']),
            DifferentValues(['Q', 'NT']),
            DifferentValues(['NT', 'Q']),
            DifferentValues(['NSW', 'Q']),
            DifferentValues(['Q', 'NSW']),
            DifferentValues(['V', 'NSW']),
            DifferentValues(['NSW', 'V'])
            ]
MapColoring = CSP(variables=map_vars,
                  domains=map_domains,
                  constraints=map_cons)
