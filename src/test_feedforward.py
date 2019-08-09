 
"""
Test the performance of the best genome produced by evolve-feedforward.py.
"""

import os
import pickle
import neat
import time
import numpy as np
from town import Town
from neat import nn

# load the winner
with open('winner-feedforward', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'neat_config.cfg')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

sim = Town()
sim = Town()
sim.load_empty_state(size=10)
sim.spawn_citizen(location=(5, 5))
sim.spawn_hunter(location=(3,3))

caught = False
max_sim_iterations = 100
iteration = 0
while iteration < max_sim_iterations:
    for citizen in sim.citizens:
        inputs = np.transpose(citizen.vision).flatten()
        print(inputs)
        print("Shape ", inputs.shape)
        citizen.action_preference = net.activate(inputs)

    print(sim)
    sim.iterate()
    time.sleep(0.1)

    for citizen in sim.citizens:
        if citizen.score["caught"]:
            caught = True
        fitness = citizen.score["survival_time"]/float(max_sim_iterations)
        print(fitness)
    if caught:
        break

    iteration += 1
