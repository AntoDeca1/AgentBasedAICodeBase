import random


def random_variable(problem, state):
    """
    Retrieve a random variable from the ones that could be selected
    :param problem:
    :param state:
    :return:
    """
    remaining_variables = problem.assignable_variables(state)
    random.shuffle(remaining_variables)
    return remaining_variables.pop()


def minimum_remaining_values(problem, state):
    """
    Choose the variable that has the fewest legal values
    :param problem:
    :param state:
    :return:
    """
    remaining_variables = problem.assignable_variables(state)
    return min(remaining_variables, key=lambda rem_var: problem.legal_moves(state, rem_var))


def degree_heuristic(problem, state):
    """
    Choose the value with the largest number of constraints
    :param problem:
    :param state:
    :return:
    """
    remaining_variables = problem.assignable_variables(state)
    return max(remaining_variables, key=lambda rem_var: problem.remaining_constraints(state, rem_var))


def random_assignment(problem, state, variable):
    """
    Return a random values from the ones in the input variable domain
    :param problem:
    :param state:
    :param variable:
    :return:
    """
    values = problem.domains[variable]
    random.shuffle(values)
    return values


def least_constraining_value(problem, state, variable):
    """
    Choose the least constraint value,the one that rules out less constraint as possible
    :param problem:
    :param state:
    :param variable:
    :return:
    """
    assignable_values = problem.domains[variable]
    return sorted(assignable_values,
                  key=lambda v: -sum([len(problem.legal_moves(problem.assign(state, variable, v), var)) for var in
                                      problem.assignable_variables(problem.assign(state, variable, v))]))



class BackTracking:
    def __init__(self, problem, var_criterion=None, value_criterion=None):
        self.problem = problem
        self.var_criterion = var_criterion
        if self.var_criterion == None:
            self.var_criterion = random_variable
        self.value_criterion = value_criterion
        if self.value_criterion == None:
            self.value_criterion = random_assignment

    def run(self, state):
        if self.problem.goal_test(state):
            return state

        variable = self.var_criterion(self.problem, state)

        if variable is None:
            return False

        values = self.value_criterion(self.problem, state, variable)
        for value in values:
            new_state = self.problem.assign(state, variable, value)

            if self.problem.consistent(new_state):
                state = dict(new_state)

                result = self.run(dict(state))

                if result:
                    return result
                else:
                    state = self.problem.rollback(state, variable)
        return False

    def forward_checking(self, state, domains):
        """
        Riduco i domini in base allo stato attuale
        :param state:
        :param domains:
        :return:
        """
        new_domains = dict(domains)
        for var in self.problem.variables:
            new_domains[var] = self.problem.legal_moves(state, var)
        return new_domains

    def run_with_forward_checking(self, state, domains):
        # check if the state is the goal state
        if self.problem.goal_test(state):
            return state

        # check for domain failure with forward checking
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

                # apply forward checking
                new_domains = self.forward_checking(state, domains)
                del (new_domains[variable])

                # run the search on the new state
                result = self.run_with_forward_checking(dict(state), new_domains)

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)

        # if there is no possible value a failure
        return False
