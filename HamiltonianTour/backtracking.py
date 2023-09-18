import random
from NQueensCSP.ac3 import AC3


def random_variable(problem, state):
    """
    Given a state returns checks the possible assignable variables(the one not in the state yet)
    and return one of them randomly,this is what we do when we decide to not to use heuristics
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


def minimum_remaining_values(problem, state):
    """
    Choose the variable with the fewest legal values
    @param problem: a CSP problem
    @param state: a state
    @return: a variable
    """
    return min(problem.assignable_variables(state), key=lambda v: len(problem.legal_moves(state, v)))


def degree_heuristic(problem, state):
    """
    Choose the variable with the most constraints on remaining variables
    @param problem: a CSP problem
    @param state: a state
    @return: a variable
    """
    return max(problem.assignable_variables(state), key=lambda v: problem.remaining_constraints(state, v))


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
    WORKFLOW:Per ogni valore controlla
    1)Le variabili assegnabili se assegno alla variabile in input il particolare valore
    ("Cosa succede se assegno alla variabile in input questo valore)
    2) Per le variabili a assegnabili calcolo il numero di valori assegnabili per ogni variabile
    """
    assignable_values = problem.domains[variable]
    return sorted(assignable_values,
                  key=lambda v: -sum([len(problem.legal_moves(problem.assign(state, variable, v), var))
                                      for var in problem.assignable_variables(problem.assign(state, variable, v))]))


class BackTracking:
    def __init__(self, problem, var_criterion, value_criterion):
        self.problem = problem
        self.var_criterion = var_criterion
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

    def ac3_online(self, state, variable):

        assignable_variables = self.problem.assignable_variables(state)

        ac3_state = {k: v for (k, v) in state.items() if k == variable}

        queue = [c for c in self.problem.constraints if
                 c.variables[0] in assignable_variables and c.variables[1] == variable]
        while queue:

            if 0 in [len(v) for k, v in self.problem.domains.items()]:
                return False

            arc = queue.pop()

            if self.problem.remove_inconsistent_values(arc=arc, actual_state=ac3_state):
                all_arcs_to_be_checked = [c for c in self.problem.constraints if
                                          c.variables[0] in assignable_variables and c.variables[1] == variable]
                variable_1, _ = arc.variables
                neighbours = [arc for arc in all_arcs_to_be_checked if arc.variables[1] == variable_1]
                queue.extend(neighbours)
        return True

    def run_with_ac3_online(self, state):
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

                variable_domain = self.problem.domains[variable]
                self.problem.domains[variable] = [value]

                self.ac3_online(state, variable)

                # run the search on the new state
                result = self.run_with_ac3_online(dict(state))

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)
                    self.problem.domains[variable] = variable_domain

                    # if there is no possible value a failure
        return False
