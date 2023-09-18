from ClassSchedulingLocal.environment import classes
from ClassSchedulingLocal.local_search import *


class SchedulingProblem:

    def __init__(self, calendar, initial_state=None):
        self.calendar = calendar
        self.initial_state = initial_state
        if self.initial_state is None:
            self.initial_state = {}

    def conflicts(self, state):
        conflicts = 0
        if "Class1" in state and "Class2" in state:
            if state["Class1"] == state["Class2"]:
                conflicts += 1
        if "Class2" in state and "Class3" in state:
            if state["Class2"] == state["Class3"]:
                conflicts += 1
        if "Class2" in state and "Class4" in state:
            if state["Class2"] == state["Class4"]:
                conflicts += 1
        if "Class3" in state and "Class4" in state:
            if state["Class3"] == state["Class4"]:
                conflicts += 1
        return conflicts

    def actions(self, state):
        actions = []
        for section in self.calendar:
            if section not in state:
                for professor in self.calendar[section]["Professors"]:
                    actions.append((section, professor))
        return actions

    def goal_test(self, state):
        if len(state) == len(self.calendar) and self.conflicts(state) == 0:
            return True
        else:
            return False

    def random_state(self):
        new_state = {}
        for section in self.calendar:
            new_state[section] = random.choice(self.calendar[section]["Professors"])
        return new_state

    def result(self, state, action):
        new_state = dict(state)
        section, professor = action
        new_state[section] = professor
        return new_state

    def successors(self, state):
        actions = self.actions(state)
        return [self.result(state, action) for action in actions]

    def value(self, state):
        return len(state) - self.conflicts(state)


problem = SchedulingProblem(calendar=classes)
problem.actions(problem.initial_state)
# strategy = HillClimbing(problem=problem)
strategy = LocalBeamSearch(problem=problem)
print(strategy.run())
