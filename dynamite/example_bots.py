import random

"""
Just return paper
The example from dynamite.softwire.com
"""
class PaperBot:
    def __init__(self):
        pass

    def make_move(self, gamestate):
        return 'P'


"""
Random from rock, paper, scissors
"""
class RandomNoDynamiteBot:
    options = ['R', 'P', 'S']

    def make_move(self, gamestate):
        return random.choice(RandomNoDynamiteBot.options)


"""
Copy the opponent's last move
"""
class CopyOpponentsLastMoveBot:
    def make_move(self, gamestate):
        rounds = gamestate['rounds']
        if rounds:
            last_round = rounds[-1]
            opponent_move = last_round['p2']
            return opponent_move
        else:
            # First round! Open with a random non-dynamite
            return random.choice(['R', 'P', 'S', 'W'])


"""
Cycle scissors, paper, rock
"""
class CycleBackwardsBot:
    options = ['S', 'P', 'R']

    def make_move(self, gamestate):
        rounds = gamestate['rounds']
        return CycleBackwardsBot.options[len(rounds) % 3]
