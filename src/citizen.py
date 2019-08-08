import neat
import numpy as np
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

    def __init__(self, location=(0, 0)):
        # Performance evaluation criteria.
        self.score = {"caught": False,
                      "survival_time": 0,
                      "steps": 0}

        # Agent stats.
        self.label = "C"
        self.vision = np.zeros([8, 8, 2])
        self.actions = {"Up":    (0, -1),
                        "Down":  (0, 1),
                        "Left":  (-1, 0),
                        "Right": (1, 0),
                        "Stand": (0, 0)}
        self.action_keys = list(self.actions.keys())
        self.actions_len = len(self.actions)

        # Agent vars.
        self.location = np.array([location[0], location[1]])
        self.stamina = 100
        self.fast_step_counter = 0
        self.is_wounded = False

    def __repr__(self):
        return "Citizen at " + str(self.location)

    def calc_step(self):
        return self.actions[self.action_keys[randint(self.actions_len)]]

    def step(self, forced_step=None):
        return self.calc_step() if forced_step == None else forced_step

    def update_location(self, move=(0, 0)):
        self.location += move
        self.score["survival_time"] += 1
        self.score["steps"] += sum(move)


if __name__ == '__main__':
    c = Citizen()
    x = np.array([[[1, 0], [2, 3], [3, 4]]])
    # print(c.next_step())
    # print(c.vision)
