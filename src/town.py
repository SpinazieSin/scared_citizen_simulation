import numpy as np
from citizen import Citizen
from hunter import Hunter, PlayerHunter


class Town:
    """
    The town holds the representation of the game world and its objects.
    """

    def __init__(self):
        self.initial_state = []
        self.state = []
        self.objects = []
        self.object_layer = {"-": 0,
                             "B": 1,
                             "H": 2}

    def __repr__(self):
        state_string = ""
        for col in self.state:
            state_string += "".join(col) + "\n"
        return state_string

    def load_state_from_file(self, path):
        f = open(path, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            self.state.append([block for block in line[:-1]])

    def load_empty_state(self, size=50):
        self.state = [["-" for block in range(size)] for column in range(size)]
        self.int_state = np.zeros([len(self.state), len(self.state), len(self.object_layer)])

    def spawn_hunter(self, location=(0, 0)):
        self.state[location] = Hunter()

    def spawn_citizen(self, location=(0,0)):
        self.state[location] = Citizen()


if __name__ == '__main__':
    t = Town()
    # t.load_state_from_file(path="layouts/basic_layout.txt")
    t.load_empty_state()
    print(t)
    print(t.int_state)