import numpy as np
import neat as nt
from discrete import Discrete
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
        self.player_hunters = []
        self.object_layer = {"B": 0,
                             "H": 1,
                             "C": 2}
        self.object_layer_keys = ["B", "H", "C"]
        self.legal_player_moves = {"w": "Up",
                                   "a": "Left",
                                   "s": "Down",
                                   "d": "Right"}
        self.layer_size = len(self.object_layer_keys)
        self.action_space = Discrete(len(self.object_layer_keys))
        self.iteration = 0
        self.same_location = np.array([0, 0])

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
            new_x, new_y = agent.location + move
            if new_x < 0 or new_y < 0:
                return False
            for check_block in range(self.layer_size):
                if self.state[new_x, new_y, check_block] > 0:
                    return False
                else:
                    return True
        except:
            return False

    def move_agent(self, agent, move):
        self.state[(agent.location[0], agent.location[1],
                    self.object_layer[agent.label])] = 0
        agent.update_location(move)
        self.state[(agent.location[0], agent.location[1],
                    self.object_layer[agent.label])] = 1

    def iterate(self):
        # Increment step
        self.iteration += 1

        # Move players
        for agent in self.player_hunters:
            target = self.citizens[randint(len(self.citizens))]
            if False not in ((target.location - agent.location) <= (1, 1)):
                target.score["caught"] = True
            move = self.move_player(agent)
            if self.is_legal_move(move, agent):
                self.move_agent(agent, move)

        # Move hunters
        for agent in self.hunters:
            target = self.citizens[randint(len(self.citizens))]
            if False not in ((target.location - agent.location) <= (1, 1)):
                target.score["caught"] = True
            move = agent.step(target=target.location)
            if self.iteration % 3 + randint(-1, 1) == 0 and not np.array_equal(target.location - agent.location, self.same_location):
                continue
            if self.is_legal_move(move, agent):
                self.move_agent(agent, move)

        # Move citizens
        for agent in self.citizens:

            """
            vision = np.zeros([7, 7, 2])
            vision[:, :, self.object_layer["B"]] = np.ones([7, 7])
            pos_x, pos_y = agent.location
            x_max = pos_x+4
            y_max = pos_y+4
            x_min = pos_x-3
            y_min = pos_y-3

            y_index = -1
            for col in range(y_min, y_max):
                y_index += 1
                x_index = -1
                if col < 0 or col > self.size - 1:
                    continue
                for row in range(x_min, x_max):
                    x_index += 1
                    if row < 0 or row > self.size - 1:
                        continue
                    for layer in range(self.layer_size - 1):
                        object_at_pos = self.state[row, col, layer]
                        vision[x_index, y_index, layer] = object_at_pos
            """

            # agent.vision = np.ones([4, 5])
            # for search_range in [(-4, 4), (5)]:
            #     return

            closest_hunter = (100, 100)
            for hunter in self.hunters + self.player_hunters:
                hunter_distance = np.clip(
                    agent.location - hunter.location, -8, 8)/8.
                if sum(hunter_distance) < sum(closest_hunter):
                    closest_hunter = hunter_distance

            hunter_distance_max = np.ones(2)
            hunter_distance_min = np.ones(2)
            for i in range(2):
                if hunter_distance[i] < 0:
                    hunter_distance_min[i] = np.abs(closest_hunter[i])
                else:
                    hunter_distance_max[i] = closest_hunter[i]

            wall_distance_max = np.clip(np.array(
                [self.size - agent.location[0], self.size - agent.location[1]]), 0, 8)/8.
            wall_distance_min = np.clip(
                np.array([agent.location[0], agent.location[1]]), 0, 8)/8.

            # Print the vision here
            # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in vision[:,:, self.object_layer["B"]]]))
            agent.vision = np.array([hunter_distance_max,
                                     hunter_distance_min,
                                     wall_distance_max,
                                     wall_distance_min]).flatten()

            move = agent.step()
            if self.is_legal_move(move, agent):
                self.move_agent(agent, move)
    
    def step(self, action = 0):
        citizen = self.citizens[0]
        citizen.queued_action = action
        observation = citizen.vision
        self.iterate()
        reward = 1. if citizen.score["caught"] else 0.
        done = True if reward == 1 else False
        info = {}
        return observation, reward, done, info

    def reset(self):
        self.hunters = []
        self.citizens = []
        self.load_empty_state()
        self.spawn_citizen(location=(25, 25), ai_type = "rl")
        self.spawn_hunter(location=(22, 22))
        print(self.citizens[0].vision)
        print(self.citizens[0].vision.shape)
        return self.citizens[0].vision.flatten()

    def load_state_from_file(self, path):
        f = open(path, "r")
        while True:
            line = f.readline()
            if line == "":
                break
            self.state.append([block for block in line[:-1]])

    def load_empty_state(self, size=50):
        self.size = size
        self.initial_state = [
            ["-" for block in range(size)] for column in range(size)]
        self.state = np.zeros(
            [size, size, len(self.object_layer)])

    def spawn_hunter(self, location=(0, 0)):
        self.hunters.append(Hunter(location))
        self.state[(location[0], location[1], self.object_layer["H"])] = 1

    def spawn_citizen(self, location=(0, 0), ai_type="learning"):
        self.citizens.append(Citizen(location, ai_type))
        self.state[(location[0], location[1], self.object_layer["C"])] = 1

    def spawn_player(self, location=(0, 0)):
        self.player_hunters.append(Hunter(location))
        self.state[(location[0], location[1], self.object_layer["H"])] = 1

    def move_player(self, agent):
        player_input = ""
        while player_input not in self.legal_player_moves:
            player_input = input("Enter Move: ")
        return agent.actions[self.legal_player_moves[player_input]]


if __name__ == '__main__':
    t = Town()
    # t.load_state_from_file(path="layouts/basic_layout.txt")
    t.load_empty_state()
    t.spawn_citizen(location=(25, 25))
    t.spawn_hunter(location=(24, 24))
    t.iterate()
    # print(t.citizens[0].vision)
