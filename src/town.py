import numpy as np
import neat as nt
from numpy.random import randint
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
        self.hunters = []
        self.citizens = []
        self.object_layer = {"B": 0,
                             "H": 1,
                             "C": 2}
        self.object_layer_keys = ["B", "H", "C"]
        self.layer_size = len(self.object_layer_keys)

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

    def is_legal_move(self, move, agent):
        try:
            new_x = agent.location[0] + move[0]
            new_y = agent.location[1] + move[1]
            if new_x < 0 or new_y < 0: return False
            for check_block in range(self.layer_size):
                if self.state[new_x, new_y, check_block] > 0:
                    return False
                else:
                    return True
        except:
            return False

    def move_agent(self, agent, move):
        self.state[(agent.location[0], agent.location[1], self.object_layer[agent.label])] = 0
        agent.update_location(move)
        self.state[(agent.location[0], agent.location[1], self.object_layer[agent.label])] = 1

    def iterate(self):
        # Move hunters
        for agent in self.hunters:
            target = self.citizens[randint(len(self.citizens))]
            move = agent.step(target=target.location)
            if self.is_legal_move(move, agent):
                self.move_agent(agent, move)

        # Move citizens
        for agent in self.citizens:
            move = agent.step()
            if self.is_legal_move(move, agent):
                self.move_agent(agent, move)
    
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
        self.hunters.append(Hunter(location))
        self.state[(location[0], location[1], self.object_layer["H"])] = 1

    def spawn_citizen(self, location=(0, 0)):
        self.citizens.append(Citizen(location))
        self.state[(location[0], location[1], self.object_layer["C"])] = 1


if __name__ == '__main__':
    t = Town()
    # t.load_state_from_file(path="layouts/basic_layout.txt")
    t.load_empty_state()
    t.spawn_citizen(location=(25,25))
    t.iterate()
    print(t)
