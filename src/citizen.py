import neat
import numpy as np
import pickle
import os
from numpy.random import randint


class Citizen():
    """
    The idea of a citizen is to learn to run from a hunter
    and use the environment to its advantage.
    The citizen should be as annoying as possible for a hunter player
    """

    INITIAL_POPULATION_SIZE = 400
    N_PARENTS_NEW_GEN = 8
    N_MUTATED_PARENTS_NEW_GEN = 20
    N_MATES_NEW_GEN = 20
    PROB_WEIGHT_CHANGE = 0.5
    GAMMA = 0.1

    N_GEN = 100

    def __init__(self, location=(0, 0), ai_type=None):
        # Performance evaluation criteria.
        self.score = {"caught": False,
                      "survival_time": 0,
                      "steps": 0}

        # Agent stats.
        self.ai_type = ai_type
        self.label = "C"
        self.vision = np.zeros(8)
        self.actions = {"Left":    (0, -1),
                        "Right":  (0, 1),
                        "Up":  (-1, 0),
                        "Down": (1, 0),
                        "Stand": (0, 0)}
        self.action_keys = ["Left", "Right", "Up", "Down", "Stand"]
        self.actions_len = len(self.actions)

        # Agent vars.
        self.location = np.array([location[0], location[1]])
        self.stamina = 100
        self.fast_step_counter = 0
        self.is_wounded = False

        # Agent decision
        self.action_preference = [
            randint(10)/10. for i in range(len(self.action_keys))]

        # Agent brain
        try:
            with open('models/winner-feedforward.model', 'rb') as f:
                c = pickle.load(f)
            local_dir = os.path.dirname(__file__)
            config_path = os.path.join(local_dir, 'neat_config.cfg')
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 config_path)
            self.net = neat.nn.FeedForwardNetwork.create(c, config)
        except:
            self.net = None

    def __repr__(self):
        return "Citizen at " + str(self.location)

    def calc_step(self):
        # print(self.action_preference)
        # print(self.action_keys)
        # print("Doing ", self.action_keys[np.argmax(self.action_preference)])
        # print("With coords", self.actions[self.action_keys[np.argmax(self.action_preference)]])

        # print(np.argmax(self.net.activate(np.transpose(self.vision).flatten())))
        # print(self.net.activate(np.transpose(self.vision).flatten()))
        # print(self.action_keys[np.argmax(
        #     self.net.activate(np.transpose(self.vision).flatten()))])
        # return (0, 0)

        return self.actions[self.action_keys[{
            "learning": np.argmax(self.action_preference),
            "smart": np.argmax(self.net.activate(np.transpose(self.vision).flatten())),
            "random": randint(self.actions_len)}[self.ai_type]]]

    def step(self, forced_step=None):
        return self.calc_step() if forced_step == None else forced_step

    def update_location(self, move=(0, 0)):
        self.location += move
        self.score["survival_time"] += 1
        self.score["steps"] += sum(np.abs(move))


if __name__ == '__main__':
    c = Citizen()
    x = np.array([[[1, 0], [2, 3], [3, 4]]])
    # print(c.next_step())
    # print(c.vision)
