import numpy as np

phi = np.random.uniform(-1, 1)


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
        self.fitness = self.fitness_function.eval(self.x)
        self.num_trials = 0
        self.max_trials = max_trials
        self.prob = 0.0

    def generate_random_position(self):
        return np.random.uniform(self.fitness_function.init_subspace_lb,
                                 self.fitness_function.init_subspace_ub,
                                 self.search_space.num_dim)

    def reset(self):
        if self.num_trials > self.max_trials:
            self.x = self.generate_random_position()
            self.num_trials = 0
            self.fitness = self.fitness_function.eval(self.x)
            self.prob = 0.0

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
            fitness_vj = self.fitness_function.eval(v)
            if fitness_vj < self.fitness:
                self.x = v
                self.fitness = fitness_vj
                self.num_trials = 0
            else:
                self.num_trials += 1


class EmployeeBee(Bee):
    def find_new_food_source(self):
        self.produce_and_eval_new_sol()

    def calculate_prob(self, sum_fitness):
        self.prob = self.get_fitness() / sum_fitness

    def get_fitness(self):
        return 1 / (1 + self.fitness) if self.fitness >= 0 else 1 + abs(self.fitness)


class OnlookerBee(Bee):
    def exploit(self, food_sources):
        for food_source in food_sources:
            r = np.random.uniform(0, 1)
            if r < food_source.prob:
                self.produce_and_eval_new_sol()


class Colony(object):
    def __init__(self, search_space, fitness_function, size, max_trials, max_fitness_evaluations):
        self.search_space = search_space
        self.fitness_function = fitness_function
        self.size = size
        self.max_trials = max_trials
        self.max_fitness_evaluations = max_fitness_evaluations
        self.employee_bees = []
        self.onlooker_bees = []
        self.best_solution = None
        self.best_solution = []
        for idx in range(self.size // 2):
            employee_bee = EmployeeBee(self.fitness_function, self.search_space, self.max_trials)
            self.employee_bees.append(employee_bee)
            onlooker_bee = OnlookerBee(self.fitness_function, self.search_space, self.max_trials)
            self.onlooker_bees.append(onlooker_bee)

    def employee_bees_phase(self):
        for employee_bee in self.employee_bees:
            employee_bee.find_new_food_source()

    def employee_bees_sum_fitness(self):
        f = []
        for employee_bee in self.employee_bees:
            f.append(employee_bee.get_fitness())
        fsum = np.sum(np.array(f))
        return fsum

    def calculate_prob(self):
        sum_fitness = self.employee_bees_sum_fitness()
        for employee_bee in self.employee_bees:
            employee_bee.calculate_prob(sum_fitness)

    def onlooker_bees_phase(self):
        for onlooker_bee in self.onlooker_bees:
            onlooker_bee.exploit(self.employee_bees)

    def scout_bees_phase(self):
        for employee_bee in self.employee_bees:
            employee_bee.reset()
        for onlooker_bee in self.onlooker_bees:
            onlooker_bee.reset()

    def optimize(self):
        while self.fitness_function.fitness_readings_count <= self.max_fitness_evaluations:
            self.employee_bees_phase()
            self.calculate_prob()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
