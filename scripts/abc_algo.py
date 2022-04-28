import math
import numpy as np
import copy

phi = np.random.uniform(-1, 1)


class FitnessFunction(object):
    def __init__(self, lb, ub, init_subspace_lb, init_subspace_ub):
        self.lb = lb
        self.ub = ub
        self.init_subspace_lb = init_subspace_lb
        self.init_subspace_ub = init_subspace_ub
        self.fitness_readings_count = 0
        self.best_fitness = float("inf")
        self.best_fitness_list = []

    def evaluate(self, x):
        pass


class SphereFitnessFunction(FitnessFunction):
    def __init__(self):
        super(SphereFitnessFunction, self).__init__(-100.0, 100.0, 50.0, 100.0)

    def evaluate(self, x):
        fit = np.sum(x ** 2)
        # if fit < self.best_fitness:
        self.best_fitness = min(fit, self.best_fitness)
        # if self.fitness_readings_count % 10 == 0:
        self.best_fitness_list.append(self.best_fitness)
        self.fitness_readings_count += 1
        return fit


class RosenbrockFitnessFunction(FitnessFunction):
    def __init__(self):
        super(RosenbrockFitnessFunction, self).__init__(-30.0, 30.0, 15.0, 30.0)

    def evaluate(self, x):
        sum_ = 0.0
        for i in range(1, len(x) - 1):
            sum_ += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
        fit = sum_
        if fit < self.best_fitness:
            self.best_fitness = fit
        self.best_fitness_list.append(self.best_fitness)
        self.fitness_readings_count += 1
        return fit


class RastriginFitnessFunction(FitnessFunction):
    def __init__(self):
        super(RastriginFitnessFunction, self).__init__(-5.12, 5.12, 2.56, 5.12)

    def evaluate(self, x):
        f_x = [xi ** 2 - 10 * math.cos(2 * math.pi * xi) + 10 for xi in x]
        fit = sum(f_x)
        if fit < self.best_fitness:
            self.best_fitness = fit
        self.best_fitness_list.append(self.best_fitness)
        self.fitness_readings_count += 1
        return fit


class SearchSpace(object):
    def __init__(self, fitness_function, num_dim):
        self.num_dim = num_dim
        self.dim_lb = fitness_function.lb
        self.dim_ub = fitness_function.ub


class Bee(object):
    def __init__(self, fitness_function, search_space, max_trials):
        self.fitness_function = fitness_function
        self.search_space = search_space
        self.x = self.generate_random_position()
        self.fitness = self.fitness_function.evaluate(self.x)
        self.num_trials = 0
        self.max_trials = max_trials
        self.probability = 0.0

    def generate_random_position(self):
        return np.random.uniform(self.fitness_function.init_subspace_lb,
                                 self.fitness_function.init_subspace_ub,
                                 self.search_space.num_dim)

    def max_trials_reached_restart(self):
        if self.num_trials > self.max_trials:
            self.x = self.generate_random_position()
            self.num_trials = 0
            self.fitness = self.fitness_function.evaluate(self.x)
            self.probability = 0.0

    def produce_and_eval_new_sol(self):
        if self.num_trials <= self.max_trials:
            v = np.zeros((self.search_space.num_dim,), dtype=np.float)
            x_kj = np.random.choice(self.x)
            for j in range(self.search_space.num_dim):
                v[j] = self.x[j] + phi * (self.x[j] - x_kj)
                if v[j] > self.search_space.dim_ub:
                    v[j] = self.search_space.dim_ub
                if v[j] < self.search_space.dim_lb:
                    v[j] = self.search_space.dim_lb
            fitness_vj = self.fitness_function.evaluate(v)
            if fitness_vj < self.fitness:
                self.x = v
                self.fitness = fitness_vj
                self.num_trials = 0
            else:
                self.num_trials += 1


class EmployeeBee(Bee):
    def find_new_food_source(self):
        self.produce_and_eval_new_sol()

    def calculate_probability(self, sum_fitness):
        self.probability = self.get_fitness() / sum_fitness

    def get_fitness(self):
        if self.fitness >= 0:
            return 1 / (1 + self.fitness)
        else:
            return 1 + abs(self.fitness)


class OnlookerBee(Bee):
    def exploit(self, food_sources):
        for food_source in food_sources:
            r = np.random.uniform(0, 1)
            if r < food_source.probability:
                self.produce_and_eval_new_sol()


class Colony(object):
    def __init__(self, search_space, fitness_function, size, max_trials, max_fitness_evaluations):
        self.search_space = search_space
        self.fitness_function = fitness_function
        self.size = size
        self.max_trials = max_trials
        self.max_fitness_evaluations = max_fitness_evaluations
        self.employee_bees_list = []
        self.onlooker_bees_list = []
        self.best_solution = None
        self.best_solution_list = []
        for idx in range(self.size // 2):
            employee_bee = EmployeeBee(self.fitness_function, self.search_space, self.max_trials)
            self.employee_bees_list.append(employee_bee)
            onlooker_bee = OnlookerBee(self.fitness_function, self.search_space, self.max_trials)
            self.onlooker_bees_list.append(onlooker_bee)

    def employee_bees_phase(self):
        for employee_bee in self.employee_bees_list:
            employee_bee.find_new_food_source()

    def employee_bees_sum_fitness(self):
        f = []
        for employee_bee in self.employee_bees_list:
            f.append(employee_bee.get_fitness())
        sum = np.sum(np.array(f))
        self.new_sol.append(min(f))
        return sum

    def calculate_probabilities(self):
        sum_fitness = self.employee_bees_sum_fitness()
        for employee_bee in self.employee_bees_list:
            employee_bee.calculate_probability(sum_fitness)

    def onlooker_bees_phase(self):
        for onlooker_bee in self.onlooker_bees_list:
            onlooker_bee.exploit(self.employee_bees_list)

    def scout_bees_phase(self):
        for employee_bee in self.employee_bees_list:
            employee_bee.max_trials_reached_restart()
        for onlooker_bee in self.onlooker_bees_list:
            onlooker_bee.max_trials_reached_restart()

    def memorize_best_solution(self):
        for employee_bee in self.employee_bees_list:
            if not self.best_solution or employee_bee.fitness < self.best_solution.fitness:
                self.best_solution = copy.copy(employee_bee)
                self.best_solution_list.append(self.best_solution)

        for onlooker_bee in self.onlooker_bees_list:
            if not self.best_solution or onlooker_bee.fitness < self.best_solution.fitness:
                self.best_solution = copy.copy(onlooker_bee)
                self.best_solution_list.append(self.best_solution)

    def optimize(self):
        while self.fitness_function.fitness_readings_count <= self.max_fitness_evaluations:
            self.employee_bees_phase()
            self.calculate_probabilities()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            # self.memorize_best_solution()
            # print("fitness_readings_count: {} = best_fitness: {}".format(self.fitness_function.fitness_readings_count, "%04.03e" % self.best_solution.fitness))
