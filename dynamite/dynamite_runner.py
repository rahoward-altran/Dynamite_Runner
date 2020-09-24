import json

from dynamite.example_bots import *

WIN_COUNT = 1000
MAX_COUNT = 2500
DYNAMITES = 100

class DynamiteRunner:

    def __init__(self):
        self.move_dict_1 = {'rounds': []}
        self.move_dict_2 = {'rounds': []}
        self.bot_1 = CycleBackwardsBot()
        self.bot_2 = RandomNoDynamiteBot()
        self.draw_multiplier = 1
        self.bot_1_wins = 0
        self.bot_2_wins = 0
        self.bot_1_dynamites_used = 0
        self.bot_2_dynamites_used = 0
        self.outcome = None
        self.turn_count = 0
        self.win_map = self.load_win_map()

    @staticmethod
    def load_win_map():
        with open("win_map.json") as json_file:
            return json.load(json_file)

    def run(self):
        while not self.outcome:
            self.do_turn()
            self.check_if_bot_has_reached_1000_wins()
            if self.turn_count == MAX_COUNT:
                break
        print("bot_1: %i, bot_2: %i, turns: %i" % (self.bot_1_wins, self.bot_2_wins, self.turn_count))
        if self.outcome:
            print(self.outcome)

    def check_if_bot_has_reached_1000_wins(self):
        if not self.outcome:
            if self.bot_1_wins >= WIN_COUNT:
                self.outcome = "bot_1 wins"
            elif self.bot_2_wins >= WIN_COUNT:
                self.outcome = "bot_2 wins"

    def do_turn(self):
        bot_1_move = self.bot_1.make_move(self.move_dict_1)
        bot_2_move = self.bot_2.make_move(self.move_dict_2)
        self.move_dict_1['rounds'].append({'p1': bot_1_move, 'p2': bot_2_move})
        self.move_dict_2['rounds'].append({'p1': bot_2_move, 'p2': bot_1_move})
        self.track_dynamite_usage(bot_1_move, bot_2_move)
        self.update_win_stats(bot_1_move, bot_2_move)
        self.turn_count += 1

    def track_dynamite_usage(self, bot_1_move, bot_2_move):
        if bot_1_move == 'D':
            self.bot_1_dynamites_used += 1
            if self.bot_1_dynamites_used > DYNAMITES:
                self.outcome = "bot_1 used too many dynamites"
        if bot_2_move == 'D':
            self.bot_2_dynamites_used += 1
            if self.bot_2_dynamites_used > DYNAMITES:
                self.outcome = "bot_2 used too many dynamites"
                if self.bot_1_dynamites_used > DYNAMITES:
                    self.outcome = "both bots used too many dynamites"

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