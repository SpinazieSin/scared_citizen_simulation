import numpy as np
from citizen import Citizen
from hunter import Hunter, PlayerHunter

class Town:
    """
    The town holds the representation of the game world and its objects.
    """
    def __init__(self):
        state = np.array([50, 50])
        objects = []