import random


class ArsonistFighter:
    def __init__(self):
        self.dynamite_left = 100

    def make_move(self, gamestate):
        # Makes a random move. Does not use more than 100 dynamite limit
        if self.dynamite_left == 0:
            return self.random_move()
        else:
            self.dynamite_left -= 1
            return "D"

    def random_move(self):
        # Makes a random move. Does not use more than 100 dynamite limit
        move = random.randint(0, 3)

        if move == 0:
            return "W"
        elif move == 1:
            return "R"
        elif move == 2:
            return "P"
        elif move == 3:
            return "S"

