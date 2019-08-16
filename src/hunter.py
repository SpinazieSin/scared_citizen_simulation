import numpy as np
from numpy.random import randint


class Hunter():
    """
    You might not know this
    but this hunter is secretly a vicious grandma

    Automatic pathing for simulation is done using A star,
    """

    def __init__(self, location=(0, 0)):
        self.actions = {"Left":    (0, -1),
                        "Right":  (0, 1),
                        "Up":  (-1, 0),
                        "Down": (1, 0),
                        "Stab": (0, 0)}
        self.action_keys = ["Left", "Right", "Up", "Down" "Stab"]
        self.actions_len = len(self.actions)

        self.label = "H"
        self.location = np.array([location[0], location[1]])

    def __repr__(self):
        return "Hunter at " + str(self.location)

    def calc_step(self, target=None):
        # Nested try except for two cases.
        # First in case target is undefined, second for divide by 0.
        try:
            heuristic = target - self.location
            # if 0 in heuristic:
            #     return (0, 0)
            try:
                if np.abs(heuristic[0]) >= np.abs(heuristic[1]):
                    return (int(heuristic[0]/np.abs(heuristic[0])), 0)
                else:
                    return (0, int(heuristic[1]/np.abs(heuristic[1])))
            except:
                return (0, 0)
        except:
            return self.actions[self.action_keys[randint(self.actions_len)]]

    def step(self, forced_step=None, target=None):
        return self.calc_step(target) if forced_step == None else forced_step

    def update_location(self, move=(0, 0)):
        self.location += move


class PlayerHunter():
    """
    The user is also able to take control of the hunter for testing.
    """

    def __init__(self):
        pass


if __name__ == '__main__':
    pass
