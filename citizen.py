import numpy as np
from numpy.random import randint


class Citizen():
    """
    The idea of a citizen is to learn to run from a hunter
    and use the environment to its advantage.
    The citizen should be as annoying as possible for a hunter player
    """

    def __init__(self):
        # Performance evaluation criteria.
        self.score = {"caught": False,
                      "survival_time": 0,
                      "steps": 0}

        # Agent stats.
        self.vision = np.zeros([8, 8, 2])
        self.actions = ("Up", "Down", "Left", "Right", "Stand")
        self.actions_len = len(self.actions)
        self.stamina = 100

        # Agent vars.
        self.fast_step_counter = 0
        self.is_wounded = False

    def next_step(self):
        return self.actions[randint(self.actions_len)]


if __name__ == '__main__':
    c = Citizen()
    print(c.next_step())
    print(c.vision)
