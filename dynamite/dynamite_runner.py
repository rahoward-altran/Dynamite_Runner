import json

from dynamite.bots.big_snip import BigSnip
from dynamite.bots.paper_bot import PaperBot
from dynamite.bots.stoner import Stoner

from dynamite.bots.random_moves import RandomMoves

from dynamite.bots.arsonist_firefighter import ArsonistFirefighter
from dynamite.bots.arsonist_fighter import ArsonistFighter

# from dynamite.example_bots import *

WIN_COUNT = 1000
MAX_COUNT = 2500
DYNAMITES = 100
PRINT_EVERY = 100


class DynamiteRunner:
    valid_moves = {'R', 'P', 'S', 'D', 'W'}

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


        self.draw_count = 0
        self.outcome = None
        self.print_buffer = []

        self.win_map = self.load_win_map()

        self.bot_1_name = type(self.bot_1).__name__
        self.bot_2_name = type(self.bot_2).__name__
        if self.bot_1_name == self.bot_2_name:
            self.bot_1_name += ' 1'
            self.bot_2_name += ' 2'

    @staticmethod
    def load_win_map():g
        with open("win_map.json") as json_file:
            return json.load(json_file)

    def run(self):
        print("%s vs %s\n" % (self.bot_1_name, self.bot_2_name))
        
        while self.bot_not_reached_1000_wins() and self.invalid_move_count < 3:
         # while not self.outcome
            try:
                self.do_turn()
                # self.maybe_print_rounds()
                # self.check_if_bot_has_reached_1000_wins()
            
                if self.turn_count == MAX_COUNT:
                    break
                # self.print_rounds()
            except ValueError:
                print("No Dynamite Left. Invalid Move")
                self.invalid_move_count += 1

        print("%s: %i, %s: %i, turns: %i" % (type(self.bot_1).__name__, self.bot_1_wins, type(self.bot_2).__name__, self.bot_2_wins, self.turn_count))
        # if self.outcome:
        #    print(self.outcome)


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
==========================   
           
#    def check_if_bot_has_reached_1000_wins(self):
#        if not self.outcome:
#            if self.bot_1_wins >= WIN_COUNT:
#                self.outcome = "%s wins" % self.bot_1_name
#            elif self.bot_2_wins >= WIN_COUNT:
#                self.outcome = "%s wins" % self.bot_2_name
#
#    def do_turn(self):
#        try:
#            bot_1_move = self.bot_1.make_move(self.move_dict_1)
#        except BaseException as e:
#            self.outcome = "{} threw an exception {}".format(self.bot_1_name, e)
#            return
#        if bot_1_move not in DynamiteRunner.valid_moves:
#            self.outcome = "{} returned invalid move '{}'".format(self.bot_1_name, bot_1_move)
#            return
#        try:
#            bot_2_move = self.bot_2.make_move(self.move_dict_2)
#        except BaseException as e:
#            self.outcome = "{} threw an exception {}".format(self.bot_2_name, e)
#            return
#        if bot_2_move not in DynamiteRunner.valid_moves:
#            self.outcome = "{} returned invalid move '{}'".format(self.bot_2_name, bot_2_move)
#            return
#        self.move_dict_1['rounds'].append({'p1': bot_1_move, 'p2': bot_2_move})
#        self.move_dict_2['rounds'].append({'p1': bot_2_move, 'p2': bot_1_move})
#        self.track_dynamite_usage(bot_1_move, bot_2_move)
#>>>>>>> 02c5f15e06a0ff5f85cf8a0f2f8085e24792373c
        #self.update_win_stats(bot_1_move, bot_2_move)
        #self.update_dynamite_count(bot_1_move, bot_2_move)
        #self.turn_count += 1

    def track_dynamite_usage(self, bot_1_move, bot_2_move):
        if bot_1_move == 'D':
            self.bot_1_dynamites_used += 1
            if self.bot_1_dynamites_used > DYNAMITES:
                self.outcome = "%s used too many dynamites" % self.bot_1_name
        if bot_2_move == 'D':
            self.bot_2_dynamites_used += 1
            if self.bot_2_dynamites_used > DYNAMITES:
                self.outcome = "%s used too many dynamites" % self.bot_2_name
                if self.bot_1_dynamites_used > DYNAMITES:
                    self.outcome = "both bots used too many dynamites"

    def update_win_stats(self, bot_1_move, bot_2_move):
        win_id = self.win_map[bot_1_move][bot_2_move]
        if win_id == 'W':
            winner = 1
            self.bot_1_wins += self.draw_rollover + 1
            self.draw_rollover = 0
        elif win_id == 'L':
            winner = 2
            self.bot_2_wins += self.draw_rollover + 1
            self.draw_rollover = 0
        else:
            winner = 0
            self.draw_count += 1
            self.draw_rollover += 1
        self.print_buffer.append([bot_1_move, bot_2_move, winner])

    def update_dynamite_count(self, bot_1_move, bot_2_move):
        if bot_1_move == "D":
            self.bot_1_dynamite_used += 1
        if bot_2_move == "D":
            self.bot_2_dynamite_used += 1
   
    def maybe_print_rounds(self):
        if len(self.print_buffer) >= PRINT_EVERY:
            self.print_rounds()

    def print_rounds(self):
        if self.print_buffer:
            # Print five lines: bot_1 win flags, bot_1 moves, bot_2 moves, bot_2 win flags, blank
            first_round = self.turn_count - len(self.print_buffer)
            print('{:15}'.format(str(first_round)) + ''.join([('*' if h[2] == 1 else ' ') for h in self.print_buffer]))
            print('{:15}'.format(self.bot_1_name[:14]) + ''.join([h[0] for h in self.print_buffer]))
            print('{:15}'.format(self.bot_2_name[:14]) + ''.join([h[1] for h in self.print_buffer]))
            print('               ' + ''.join([('*' if h[2] == 2 else ' ') for h in self.print_buffer]))
            print()
            self.print_buffer = []


if __name__ == "__main__":
    DynamiteRunner().run()
