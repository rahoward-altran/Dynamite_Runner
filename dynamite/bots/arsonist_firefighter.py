class ArsonistFirefighter:
    def __init__(self):
        self.dynamite_left = 100

    def make_move(self, gamestate):
        # Makes a random move. Does not use more than 100 dynamite limit
        if self.dynamite_left == 0:
            return "W"
        else:
            self.dynamite_left -= 1
            return "D"
