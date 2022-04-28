import json

from scripts.abc_algo import *
from scripts.test_functions import *

D = 3  # dimensions
SN = 30  # population size
max_trials = 100
max_fitness_evaluations = 100000
MCN = 30

problems = {
    "Sphere": SphereFitnessFunction(),
    "Rosenbrock": RosenbrockFitnessFunction(),
    "Rastrigin": RastriginFitnessFunction()}

for problem in problems:

    res_dic = {}

    for num_exec in range(MCN):
        fitness_function = problems[problem]

        search_space = SearchSpace(fitness_function, D)
        colony = Colony(search_space, fitness_function, SN, max_trials, max_fitness_evaluations)
        colony.optimize()

        res_dic[num_exec] = fitness_function.best_fitness_list

    with open(str(problem) + '_abc.json', 'w') as js:
        json.dump(res_dic, js)
