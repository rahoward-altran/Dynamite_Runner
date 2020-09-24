import json

from dynamite.example_bots import *

WIN_COUNT = 1000
MAX_COUNT = 2500


class DynamiteRunner:

    def __init__(self):
        self.move_dict_1 = {'rounds': []}
        self.move_dict_2 = {'rounds': []}
        self.bot_1 = CycleBackwardsBot()
        self.bot_2 = RandomNoDynamiteBot()
        self.draw_multiplier = 1
        self.bot_1_wins = 0
        self.bot_2_wins = 0
        self.turn_count = 0
        self.win_map = self.load_win_map()

    @staticmethod
    def load_win_map():
        with open("win_map.json") as json_file:
            return json.load(json_file)

    def run(self):
        while self.bot_reached_1000_wins():
            self.do_turn()
            if self.turn_count == MAX_COUNT:
                break
        print("bot_1: %i, bot_2: %i, turns: %i" % (self.bot_1_wins, self.bot_2_wins, self.turn_count))

    def bot_reached_1000_wins(self):
        return self.bot_1_wins < WIN_COUNT and self.bot_2_wins < WIN_COUNT

    def do_turn(self):
        bot_1_move = self.bot_1.make_move(self.move_dict_1)
        bot_2_move = self.bot_2.make_move(self.move_dict_2)
        self.move_dict_1['rounds'].append({'p1': bot_1_move, 'p2': bot_2_move})
        self.move_dict_2['rounds'].append({'p1': bot_2_move, 'p2': bot_1_move})
        self.update_win_stats(bot_1_move, bot_2_move)
        self.turn_count += 1

    def update_win_stats(self, bot_1_move, bot_2_move):
        win_id = self.win_map[bot_1_move][bot_2_move]
        if win_id == 'W':
            self.bot_1_wins += self.draw_multiplier
            self.draw_multiplier = 1
        elif win_id == 'L':
            self.bot_2_wins += self.draw_multiplier
            self.draw_multiplier = 1
        else:
            self.draw_multiplier += 1


if __name__ == "__main__":
    DynamiteRunner().run()