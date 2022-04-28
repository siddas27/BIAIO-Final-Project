from niapy.algorithms.basic import ParticleSwarmAlgorithm, BacterialForagingOptimization, DifferentialEvolution
from niapy.task import Task

# we will run 10 repetitions of Weighted, velocity clamped PSO on the Pinter problem
for i in range(10):
    task = Task(problem='sphere', dimension=10, max_evals=100000)
    algorithm = ParticleSwarmAlgorithm(population_size=100, w=0.9, c1=0.5, c2=0.3, min_velocity=-1, max_velocity=1)
    best_x, best_fit = algorithm.run(task)
    print(best_fit)