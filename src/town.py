import numpy as np
import neat as nt
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
        self.object_layer = {"B": 0,
                             "H": 1,
                             "C": 2}
        self.object_layer_keys = ["B", "H", "C"]

    def __repr__(self):
        state_string = ""
        for col in self.state:
            row_rep = ""
            for row in col:
                b = "-"
                for i in range(len(row)):
                    if row[i] > 0:
                        b = self.object_layer_keys[i]
                        break
                row_rep += b
            state_string += row_rep + "\n"
        return state_string

    def iterate(self):
        for agent in self.objects:
            move = agent.step()
            print(move)
            agent.update_location(move)

    def load_state_from_file(self, path):
        f = open(path, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            self.state.append([block for block in line[:-1]])

    def load_empty_state(self, size=50):
        self.size = size
        self.initial_state = [["-" for block in range(size)] for column in range(size)]
        self.state = np.zeros(
            [size, size, len(self.object_layer)])

    def spawn_hunter(self, location=(0, 0)):
        self.objects.append(Hunter(location))
        self.state[(location[0], location[1], self.object_layer["H"])] = 1

    def spawn_citizen(self, location=(0, 0)):
        self.objects.append(Citizen(location))
        self.state[(location[0], location[1], self.object_layer["C"])] = 1


if __name__ == '__main__':
    t = Town()
    # t.load_state_from_file(path="layouts/basic_layout.txt")
    t.load_empty_state()
    t.spawn_citizen()
    t.iterate()
    print(t)
    print(t.objects[0].location)