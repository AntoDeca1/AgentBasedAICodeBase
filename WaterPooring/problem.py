class WaterPouring:

    def __init__(self, goal=4, capacities=(5, 3), initial_state=None):
        self.initial_state = initial_state
        if self.initial_state is None:
            self.initial_state = (0, 0)
        self.goal = goal
        self.capacities = capacities

    def successors(self, state):
        actions = self.actions(state)
        successors = [(self.result(state, action), action) for action in actions]
        return successors

    def actions(self, state):
        actions = []
        gallons_0, gallons_1 = state

        # Fill the first tank
        if gallons_0 < self.capacities[0]:
            actions.append((self.fill, 0, "#"))
            if gallons_1 != 0:
                # If the second tank is not empty and the second is not full
                actions.append((self.pour, 1, 0))

        # Fill the second tank
        if gallons_1 < self.capacities[1]:
            actions.append((self.fill, 1, "#"))
            if gallons_0 != 0:
                # If the first tank is not empty and the second is not full
                actions.append((self.pour, 0, 1))

        # If the first tank is not empty
        if gallons_0 > 0:
            actions.append((self.dump, 0, "#"))

        # If the second tank is not empty
        if gallons_1 > 0:
            actions.append((self.dump, 1, "#"))
        return actions

    def fill(self, state, gallon, _=None):
        new_state = list(state)
        new_state[gallon] = self.capacities[gallon]
        return tuple(new_state)

    def dump(self, state, gallon, _=None):
        new_state = list(state)
        new_state[gallon] = 0
        return tuple(new_state)

    def pour(self, state, gallon_i, gallon_j):
        moving_water = min(state[gallon_i], self.capacities[gallon_j] - state[gallon_j])
        new_state = list(state)
        new_state[gallon_i] -= moving_water
        new_state[gallon_j] += moving_water
        return tuple(new_state)

    def cost(self, state, a):
        return 1

    def h(self, state):
        return abs(self.goal - sum(state))

    def result(self, state, action):
        action, i, j = action
        return action(state, i, j)

    def goal_test(self, state):
        return sum(state) == self.goal
