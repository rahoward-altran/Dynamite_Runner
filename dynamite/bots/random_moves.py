import random


class RandomMoves:
    def __init__(self):
        self.dynamite_left = 100

    def make_move(self, gamestate):
        # Makes a random move. Does not use more than 100 dynamite limit
        if self.dynamite_left == 0:
            move = random.randint(0, 3)
        else:
            move = random.randint(0, 4)

        if move == 0:
            return "W"
        elif move == 1:
            return "R"
        elif move == 2:
            return "P"
        elif move == 3:
            return "S"
        elif move == 4:
            self.dynamite_left -= 1
            return "D"
