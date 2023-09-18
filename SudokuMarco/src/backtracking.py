import random
# from .ac3 import AC3


# VARIABLE SELECTION CRITERION
def random_variable(problem, state):
    """
    Given a state returns a possible variable to assign
    @param problem:
    @param state:
    @return:
    """
    assignable_vars = problem.assignable_variables(state)
    if assignable_vars:
        random.shuffle(assignable_vars)
        return assignable_vars.pop()
    # if there are no assignable variables
    return None


# TODO implement minimum remaining values and degree heuristic criterions
def minimum_remaining_values(problem,state):
    assignable_variables = problem.assignable_variables(state)
    return min(assignable_variables,key= lambda var:len(problem.legal_moves(state,var)))

def degree_heuristic(problem,state):
    assignable_variables = problem.assignable_variables(state)
    return max(assignable_variables, key=lambda var: problem.remaining_constraints(state,var))



# VALUE ASSIGNMENT CRITERION
def random_assignment(problem, state, variable):
    """
    Return a random value to be assigned to the variable
    @param problem: a CSP problem
    @param state: a state
    @param variable: a variable
    @return: a value for the variable
    """
    possible_values = problem.domains[variable]
    random.shuffle(possible_values)
    return possible_values


def least_constraining_value(problem, state, variable):
    """
    Given a variable, choose the least constraining value
    @param problem: a CSP problem
    @param state: a state
    @param variable: an assignable variable
    @return: a list of assignable values
    """
    assignable_values = problem.domains[variable]
    return sorted(assignable_values,
                  key=lambda v: -sum([len(problem.legal_moves(problem.assign(state, variable, v), var))
                                      for var in problem.assignable_variables(problem.assign(state, variable, v))]))


class BackTracking:

    def __init__(self, problem, var_criterion=None, value_criterion=None):
        self.problem = problem
        if var_criterion is None:
            var_criterion = random_variable
        self.var_criterion = var_criterion
        if value_criterion is None:
            value_criterion = random_assignment
        self.value_criterion = value_criterion

    def run(self, state):
        # check if the state is the goal state
        if self.problem.goal_test(state):
            return state

        # choose the next variable to be assigned
        variable = self.var_criterion(self.problem, state)
        if variable is None:
            return False

        # order the values with a desired order
        values = self.value_criterion(self.problem, state, variable)

        # for all the values
        for value in values:

            # assign the value and reach a new state
            new_state = self.problem.assign(state=state,
                                            variable=variable,
                                            value=value)
            if self.problem.consistent(new_state):
                state = dict(new_state)

                # run the search on the new state
                result = self.run(dict(state))

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)

        # if there is no possible value a failure
        return False

    # TODO implement forward checking and run with forward checking
    def forward_checking(self,state,domains):
        new_domains = dict(domains)
        for var in self.problem.variables:
            new_domains[var] = self.problem.legal_moves(state,var)
        return new_domains

    def run_with_forward_checking(self,state,domains):
        # check if the state is the goal state
        if self.problem.goal_test(state):
            return state
        # check if forward checking has removed all the values from a domain
        if [] in domains.values():
            return False
        # choose the next variable to be assigned
        variable = self.var_criterion(self.problem, state)
        if variable is None:
            return False

        # order the values with a desired order
        values = self.value_criterion(self.problem, state, variable)

        # for all the values
        for value in values:

            # assign the value and reach a new state
            new_state = self.problem.assign(state=state,
                                            variable=variable,
                                            value=value)
            if self.problem.consistent(new_state):
                state = dict(new_state)

                new_domains = self.forward_checking(state,domains)
                del(new_domains[variable])
                # run the search on the new state
                result = self.run_with_forward_checking(dict(state),new_domains)

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)

        # if there is no possible value a failure
        return False
