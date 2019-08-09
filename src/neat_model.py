import neat
import visualize
import numpy as np
import os
import pickle
from random import randint
from town import Town

runs_per_net = 5

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        sim = Town()
        sim.load_empty_state(size=10)
        sim.spawn_citizen(location=(5, 5))
        offsetx = 0
        offsety = 0
        while offsetx == 0 or offsety == 0:
            offsetx = randint(-3, 3)
            offsety = randint(-3, 3)
        sim.spawn_hunter(location=(5+offsetx, 5+offsety))

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        caught = False
        max_sim_iterations = 100
        iteration = 0
        while iteration < max_sim_iterations:
            for citizen in sim.citizens:
                inputs = np.transpose(citizen.vision).flatten()
                citizen.action_preference = net.activate(inputs)

            sim.iterate()

            for citizen in sim.citizens:
                if citizen.score["caught"]:
                    caught = True
                fitness = ((citizen.score["survival_time"]*100.)/(citizen.score["steps"]+1))/(max_sim_iterations)
                fitness = (citizen.score["survival_time"])/(max_sim_iterations)
            if caught:
                break

            iteration += 1

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return min(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config.cfg')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(6, eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward.model', 'wb') as f:
        pickle.dump(winner, f)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")
    visualize.draw_net(config, winner, True)

if __name__ == '__main__':
    run()
