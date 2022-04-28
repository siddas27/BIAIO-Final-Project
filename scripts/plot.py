import json
from typing import List

from matplotlib import pyplot as plt
from glob import glob

problems = {
    "Sphere",
    "Rosenbrock",
    "Rastrigin"}

files_list = glob('../export/*.json')
files_list.sort()

with open('../export/abc.json') as js:
    abc = json.load(js)
lim = 10
for prob in problems:

    algorithms = {
        "ParticleSwarmAlgorithm": [],
        "BacterialForagingOptimization": [],
        "DifferentialEvolution": [],
        # "ArtificialBeeColonyAlgorithm": [],
        # "SimulatedAnnealing": [],
        "CuckooSearch": []
    }

    for i, file in enumerate(files_list):
        if i == lim:
            break
        with open(file) as js:
            d = json.load(js)
        for algo in algorithms.keys():
            obj = []
            for i in range(30):
                obj.append(d[algo][prob][i][1])
            mean = sum(obj) / 30
            algorithms[algo].append(mean)

    with open(str(prob) + '_all.json', 'w') as js:
        json.dump(algorithms, js)
    itr = [i * 500 for i in range(1, lim + 1)]

    for algo in algorithms.keys():
        plt.plot(itr, algorithms[algo], label=algo)

    itr = range(500, lim * 500)
    plt.plot(itr, abc[prob][500:lim * 500], label='ArtificialBeeColonyAlgorithm')

    plt.xlabel('# function evaluations')
    plt.ylabel('best fitness')
    plt.title(f'{prob} test function')
    plt.legend()
    plt.savefig(f'{prob}_comparison1.png')
    plt.show()
    plt.close()
