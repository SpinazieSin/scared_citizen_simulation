
class Hunter():
    """
    You might not know this
    but this hunter is secretly a vicious grandma

    Automatic pathing for simulation is done using A star,
    """

    def __init__(self, location=(0, 0)):
        self.actions = ("Up", "Down", "Left", "Right", "Attack")
        self.actions_len = len(self.actions)
        self.label = "H"
        self.location = np.array([location[0], location[1]])

class PlayerHunter():
    """
    The user is also able to take control of the hunter for testing.
    """

    def __init__(self):
        pass