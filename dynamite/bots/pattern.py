class Pattern:
    def __init__(self):
        self.dynamite_left = 100
        self.i = 0

    def make_move(self, gamestate):
        if self.dynamite_left != 0:
            self.i = (self.i+1) % 4
        else:
            self.i = (self.i+1) % 5

        if self.i == 0:
            return "W"
        elif self.i == 1:
            return "R"
        elif self.i == 2:
            return "P"
        elif self.i == 3:
            return "S"
        elif self.i == 4:
            self.dynamite_left -= 1
            return "D"
