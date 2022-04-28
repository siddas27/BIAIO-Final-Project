from niapy import Runner
from niapy.algorithms.basic import (
    ParticleSwarmAlgorithm,
    BacterialForagingOptimization,
    DifferentialEvolution,
    ArtificialBeeColonyAlgorithm
)
from niapy.problems import (
    Rosenbrock,
    Sphere,
    Rastrigin
)
import time

for e in range(1,61):
    runner = Runner(
        dimension=3,
        max_evals=e*500,
        runs=30,
        algorithms=[
            ParticleSwarmAlgorithm(),
            BacterialForagingOptimization(),
            DifferentialEvolution(),
            ArtificialBeeColonyAlgorithm(),
            "SimulatedAnnealing",
            "CuckooSearch"],
        problems=[
            Sphere(dimension=3,lower=-100,upper=100),
            Rosenbrock(dimension=3),
            Rastrigin(dimension=3)
        ]
    )

    runner.run(export='json')
    time.sleep(15)