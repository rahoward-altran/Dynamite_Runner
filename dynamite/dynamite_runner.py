import json

from dynamite.bots.big_snip import BigSnip
from dynamite.bots.paper_bot import PaperBot
from dynamite.bots.stoner import Stoner

from dynamite.bots.random_moves import RandomMoves

from dynamite.bots.arsonist_firefighter import ArsonistFirefighter
from dynamite.bots.arsonist_fighter import ArsonistFighter


WIN_COUNT = 1000
MAX_COUNT = 2500


class DynamiteRunner:

    def __init__(self):
        self.bot_1 = RandomMoves()
        self.bot_2 = ArsonistFighter()

        self.draw_rollover = 0
        self.turn_count = 0
        self.bot_1_wins = 0
        self.bot_2_wins = 0
        self.bot_1_dynamite_used = 0
        self.bot_2_dynamite_used = 0
        self.invalid_move_count = 0

        self.move_dict_bot_1 = {'rounds': []}
        self.move_dict_bot_2 = {'rounds': []}

        self.win_map = self.load_win_map()

    @staticmethod
    def load_win_map():
        with open("win_map.json") as json_file:
            return json.load(json_file)

    def run(self):
        while self.bot_not_reached_1000_wins() and self.invalid_move_count < 3:
            try:
                self.do_turn()
                if self.turn_count == MAX_COUNT:
                    break
            except ValueError:
                print("No Dynamite Left. Invalid Move")
                self.invalid_move_count += 1

        print("%s: %i, %s: %i, turns: %i" % (type(self.bot_1).__name__, self.bot_1_wins, type(self.bot_2).__name__, self.bot_2_wins, self.turn_count))

        if self.bot_not_reached_1000_wins():
            print("Max turns reached! It is a draw!")
        elif self.bot_1_wins > self.bot_2_wins:
            print(type(self.bot_1).__name__, " wins!")
        else:
            print(type(self.bot_2).__name__, " wins!")

    def bot_not_reached_1000_wins(self):
        return self.bot_1_wins < WIN_COUNT and self.bot_2_wins < WIN_COUNT

    def do_turn(self):
        bot_1_move = self.bot_1.make_move(self.move_dict_bot_1)
        bot_2_move = self.bot_2.make_move(self.move_dict_bot_2)
        if bot_1_move == "D" and self.bot_1_dynamite_used > 100 or \
            bot_2_move == "D" and self.bot_2_dynamite_used > 100:
            raise ValueError
        self.move_dict_bot_1['rounds'].append({'p1': bot_1_move, 'p2': bot_2_move})
        self.update_win_stats(bot_1_move, bot_2_move)
        self.update_dynamite_count(bot_1_move, bot_2_move)
        self.turn_count += 1

    def update_win_stats(self, bot_1_move, bot_2_move):
        win_id = self.win_map[bot_1_move][bot_2_move]
        if win_id == 'W':
            self.bot_1_wins += self.draw_rollover + 1
            self.draw_rollover = 0
        elif win_id == 'L':
            self.bot_2_wins += self.draw_rollover + 1
            self.draw_rollover = 0
        else:
            self.draw_rollover += 1

    def update_dynamite_count(self, bot_1_move, bot_2_move):
        if bot_1_move == "D":
            self.bot_1_dynamite_used += 1
        if bot_2_move == "D":
            self.bot_2_dynamite_used += 1
