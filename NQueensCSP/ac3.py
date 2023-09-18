class AC3:

    def __init__(self, csp):
        self.csp = csp

    def all_arcs(self):
        """
        Retrieves all the arc.
        N.B Like we said in the theory the arc consistency needs to be true in both direction
        in order to make the graph consistent.For this reason in the file problem.py we explicitly
        :return:
        """
        return [cons for cons in self.csp.constraints if len(cons.variables) == 3]

    def add_neighbours(self, queue, arc):
        """
        Add the queue all the constraints that have the variable on the left at the right
        Example:
        X-Y
        Y->Z
        X->Y has Y on the right
        :param queue:
        :param arc:
        :return:
        """
        var, _ = arc.variables
        neighbours = [arc for arc in self.all_arcs() if arc.variables[1] == var]
        queue.extend(neighbours)

    def run(self, state):
        # TODO: Initially all the arcs needs to be checked
        queue = self.all_arcs()

        # TODO:While the queue is not empty
        while queue:
            # TODO:Se uno dei domini delle variabili si è ridotto a zero
            if 0 in [len(v) for k, v in self.csp.domains.items()]:
                return False

            arc = queue.pop()

            if self.csp.remove_inconsistent_values(arc=arc, actual_state=state):
                self.add_neighbours(queue, arc)
        return True
