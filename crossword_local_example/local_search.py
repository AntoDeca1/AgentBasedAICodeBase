import math
import random


class HillClimbing:

    def __init__(self, problem):
        self.problem = problem

    def run(self):
        state = self.problem.initial_state
        while True:
            new_states = self.problem.successors(state)

            best_successor = max(new_states, key=lambda successor: self.problem.utility(successor))
            print(
                f"CurrentUtility {self.problem.utility(state)} and best successor {self.problem.utility(best_successor)}")

            delta = self.problem.utility(best_successor) - self.problem.utility(state)

            if delta <= 0:
                return "OK", state, self.problem.utility(state)

            state = best_successor


class SimulatedAnnealing:
    def __init__(self, problem, min_temp=0, max_time=100, initial_temp=100, lam=0.001):
        self.problem = problem
        self.min_temp = min_temp
        self.max_time = max_time
        self.initial_temp = initial_temp
        self.lam = lam

    def exponential_schedule(self, time):
        return self.initial_temp * math.exp(-self.lam * time)

    def run(self):
        t = 0
        temp = self.initial_temp
        state = self.problem.initial_state
        while temp > self.min_temp and t < self.max_time:
            new_states = self.problem.successors(state)

            selected_state = random.choice(new_states)

            delta = self.problem.utility(selected_state) - self.problem.utility(state)

            if delta > 0 or random.uniform(0, 1) < math.exp(delta / temp):
                state = selected_state
            temp = self.exponential_schedule(t)
            t += 1
        return "OK", state, self.problem.utility(state)

