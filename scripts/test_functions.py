import math
import numpy as np


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

    def update(self, fit):
        self.best_fitness = min(fit, self.best_fitness)
        self.best_fitness_list.append(self.best_fitness)
        self.fitness_readings_count += 1


class SphereFitnessFunction(FitnessFunction):
    def __init__(self):
        super(SphereFitnessFunction, self).__init__(-100.0, 100.0, 50.0, 100.0)

    def evaluate(self, x):
        fit = np.sum(x ** 2)
        self.update(fit)
        return fit


class RosenbrockFitnessFunction(FitnessFunction):
    def __init__(self):
        super(RosenbrockFitnessFunction, self).__init__(-30.0, 30.0, 15.0, 30.0)

    def evaluate(self, x):
        fit = 0.0
        for i in range(1, len(x) - 1):
            fit += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
        self.update(fit)
        return fit


class RastriginFitnessFunction(FitnessFunction):
    def __init__(self):
        super(RastriginFitnessFunction, self).__init__(-5.12, 5.12, 2.56, 5.12)

    def evaluate(self, x):
        f_x = [xi ** 2 - 10 * math.cos(2 * math.pi * xi) + 10 for xi in x]
        fit = sum(f_x)
        self.update(fit)
        return fit