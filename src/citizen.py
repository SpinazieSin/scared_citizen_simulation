import numpy as np

class Citizen():
    """
    The idea of a citizen is to learn to run from a hunter
    and use the environment to its advantage.
    The citizen should be as annoying as possible for a hunter player
    """
    
    def __init__(self):
        vision = np.array([8, 8])