import random


class SmartBot:
    def __init__(self):
        self.dynamite_left = 100
        self.opponent_dynamite_left = 100
        self.opponent_fav_move = None
        self.confidence = 0  # finite state of faith in opponents fav move
        # self.opponents_last_10 = ""

    def make_move(self, gamestate):
        self.update_info_on_opponent(gamestate['rounds'])

    def update_info_on_opponent(self, rounds_list):
        last_round = rounds_list[-1]
        if last_round