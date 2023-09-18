import math

import numpy as np
import random


class HillClimbing:
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        state = self.problem.initial_state
        while True:
            new_states = self.problem.successors(state)
            best_successor = min(new_states, key=lambda state: self.problem.conflicts(state))
            delta = self.problem.value(best_successor) - self.problem.value(state)
            if delta <= 0:
                return state, self.problem.conflicts(state)
            state = best_successor


class SimulatedAnnealing:
    def __init__(self, problem, initial_temp=100, min_temp=0, max_time=100):
        self.problem = problem
        self.initial_temp = initial_temp
        self.min_temp = min_temp
        self.max_time = max_time

    def exp_schedule(self, time, lmd=0.001):
        return self.initial_temp * np.exp(-lmd * time)

    def run(self):
        t = 0
        temp = self.initial_temp
        state = self.problem.initial_state
        while temp > self.min_temp and t < self.max_time:
            new_states = self.problem.successors(state)
            next_state = random.choice(new_states)
            delta = self.problem.value(next_state) - self.problem.value(state)
            if delta > 0 or random.uniform(0, 1) < math.exp(delta / temp):
                state = next_state

            temp = self.exp_schedule(t)
            t += 1
        return state, self.problem.value(state)


class GeneticAlghoritm:
    def __init__(self, problem, population_size=100, p=2, mutation_prob=0.2, generations=100):
        self.problem = problem
        self.population_size = population_size
        self.p = p
        self.mutation_prob = mutation_prob
        self.generations = generations

    def cross_over(self, couple):
        state_1, state_2 = couple
        split_index = np.random.randint(len(state_1))
        new_state = tuple(state_1[:split_index]) + tuple(state_2[split_index:])
        return new_state

    def mutation(self, state):
        if random.uniform(0, 1) < self.mutation_prob:
            random_index = np.random.randint(0, len(state))
            random_number = np.random.randint(0, len(state))
            temp = list(state)
            temp[random_index] = random_number
            return tuple(temp)
        return state

    def selection(self, population):
        fitnesses = list(map(lambda p: self.problem.value(p), population))
        return random.choices(population, weights=fitnesses, k=2)

    def run(self):
        population = [self.problem.random_state() for _ in range(self.population_size)]
        for i in range(self.generations):
            population = [self.mutation(self.cross_over(self.selection(population))) for _ in
                          range(self.population_size)]
        best_value = max(population, key=lambda x: self.problem.value(x))
        return best_value, self.problem.value(best_value)


class LocalBeamSearch:

    def __init__(self, problem, k=10):
        self.problem = problem
        self.k = k

    def run(self):
        # TODO:Select k random states
        states = [self.problem.random_state() for _ in range(self.k)]
        # TODO:We keep track of the best value until now
        best_state = max(states, key=lambda state: self.problem.value(state))
        while True:
            successors = []
            # TODO:For each of the k states we expand the successors
            for state in states:
                successors.extend(self.problem.successors(state))
            best_successor = max(successors, key=lambda successor: self.problem.value(successor))
            # TODO:From the whole list of successor we see if one of them satisfy the goal_test(0 conflicts)
            if self.problem.goal_test(best_successor):
                return best_successor, self.problem.conflicts(best_successor)
            # TODO:We select the best k successors
            states = sorted(successors, key=lambda successor: -self.problem.value(successor))[:self.k]
            new_state = states[0]
            # TODO:If the best successors is better we continue the search starting from the new k best nodes
            if self.problem.value(new_state) > self.problem.value(best_state):
                best_state = new_state
            else:
                return best_state, self.problem.conflicts(best_state)
