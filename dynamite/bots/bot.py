import random

EMPTY_DYNAMITE = 0
FULL_DYNAMITE = 100
DYNAMITE_THRESHOLD = 5
CONFIDENCE_THRESHOLD = 5
CONFIDENCE_HIT = 3
NO_CONFIDENCE = 0
A_LOWER = 96
HIGH_CHANCE = 20

WINDOW_SIZE = 10

class NewBot:
    def __init__(self):
        # todo: reconsider? always not use at least one dynamite so opponent's logic can't be certain I won't use it
        self.dynamite_left = FULL_DYNAMITE - 1
        self.opponent_dynamite_left = FULL_DYNAMITE

        self.opponent_move_usage = {'W': 0, 'D': 0, 'R': 0, 'S': 0, 'P': 0}
        self.opponent_fav_move = ("", 0)
        self.confidence = 0  # state of faith in opponents fav move

        self.my_last_moves_window = []
        self.opponent_last_move_window = []
        self.last_results_window = []

        self.win_map = {
            "R": {"R": "D", "P": "L", "S": "W", "D": "L", "W": "W"},
            "P": {"R": "W", "P": "D", "S": "L", "D": "L", "W": "W"},
            "S": {"R": "L", "P": "W", "S": "D", "D": "L", "W": "W"},
            "D": {"R": "W", "P": "W", "S": "W", "D": "D", "W": "L"},
            "W": {"R": "L", "P": "L", "S": "L", "D": "W", "W": "D"}
        }

    def make_move(self, gamestate):
        self.update_knowledge(gamestate['rounds'])

        if self.is_correlation():
            return self.beat_their_favourite(self.opponent_last_move_window[-1])

        # if confident with fav move play opposite
        # else random - if no dynamite don't play water
        if self.confidence >= CONFIDENCE_THRESHOLD:
            move = self.beat_their_favourite()
        else:
            move = self.random_attack()
        self.update_last_10(move)
        return move

    def update_knowledge(self, rounds_list):
        if not rounds_list:
            return
        last_round = rounds_list[-1]

        self.update_opponent_move_usage(last_round)
        self.update_opponent_fav_move()

        if len(self.opponent_last_move_window) == WINDOW_SIZE:
            self.opponent_last_move_window.pop(0)
            self.last_results_window.pop(0)
        self.opponent_last_move_window.append(last_round['p2'])
        self.last_results_window.append(self.get_result(last_round))

    def update_opponent_move_usage(self, last_round):
        if last_round['p2'] == "D":
            self.opponent_dynamite_left -= 1
            self.opponent_move_usage["D"] += 1
        elif last_round['p2'] == "W":
            self.opponent_move_usage["W"] += 1
        elif last_round['p2'] == "R":
            self.opponent_move_usage["R"] += 1
        elif last_round['p2'] == "P":
            self.opponent_move_usage["P"] += 1
        elif last_round['p2'] == "S":
            self.opponent_move_usage["S"] += 1

    def update_opponent_fav_move(self):
        most_used_move = self.opponent_fav_move[0]
        most_used_move_value = self.opponent_fav_move[1]
        # if they have used most of their dynamite then it will never be their favourite move again
        # remove from list so don't risk using water
        if self.opponent_dynamite_left < DYNAMITE_THRESHOLD:
            self.opponent_move_usage['D'] = 0
            # if it was their favourite - reset favourite
            if most_used_move == 'D':
                most_used_move = ''
                most_used_move_value = 0

        for move, usage in self.opponent_move_usage.items():
            # if joint first then pick one last one in list and lower confidence
            if usage >= most_used_move_value:
                most_used_move_value = usage
                most_used_move = move

        if self.opponent_fav_move[0] != most_used_move:
            #change in favourite
            self.confidence = NO_CONFIDENCE
        else:
            #no change in favourite confidence grows
            self.confidence += 1
            # but if we lost playing 'beat the favourite last time
            if self.last_results_window[-1] == "L":
                self.confidence = max(self.confidence - CONFIDENCE_HIT, 0)
        self.opponent_fav_move = (most_used_move, most_used_move_value)

    def beat_their_favourite(self, fav=None):
        if fav is None:
            fav = self.opponent_fav_move[0]
        winning_moves = []
        for move, result in self.win_map[fav].items():
            if result == "W" or result == "D":
                continue
            # only consider winning moves (moves that will make their favourite move lose)
            winning_moves.append(move)
        if len(winning_moves) == 1:
            # their favourite is dynamite
            #todo: NOT HERE... check they still have dynamite ...
            # todo... if they don't remove it as their favourite and reset confidence to 0
            return winning_moves[0]
            # only use dynamite when not confident with a win?
        elif len(winning_moves) == 3:
            # their favourite is water
            # hit them with rock, paper or scissors randomly
            move = random.randint(0, 2)
            return winning_moves[move]
        # their favourite is rock, paper or scissors
        # don't waste dynamite as confident level is above threshold
        winning_moves.remove('D') # todo: reconsider - might as well use them all
        return winning_moves[0]

    def random_attack(self):
        # get last move don't use dynamite twice in a row
        try:
            if self.my_last_moves_window[-1] == "D":
                chance = 0
            else:
                chance = HIGH_CHANCE
        except IndexError:
            chance = HIGH_CHANCE
        # low confidence - higher use of dynamite if available
        if self.dynamite_left == EMPTY_DYNAMITE or chance == 0:
            move = random.randint(1, 3)
        else:
            move = random.randint(1, HIGH_CHANCE)
        # Never uses water when not confident. risks are too high
        # todo:  reconsider
        # if move == 0:
        #     return "W"
        if move == 1:
            return "R"
        elif move == 2:
            return "P"
        elif move == 3:
            return "S"
        elif move >= 4:
            self.dynamite_left -= 1
            return "D"

    def update_last_10(self, new_move):
        if len(self.my_last_moves_window) == WINDOW_SIZE:
            self.my_last_moves_window.pop(0)
        self.my_last_moves_window.append(new_move)

    def get_result(self, last_round):
        return self.win_map[last_round['p1']][last_round['p2']]

    def is_correlation(self):
        try:
            a = self.my_last_moves_window[:-1]
            b = self.opponent_last_move_window[1:]
            r = [x for x in range(len(a)) if a[x: x + len(b)] == b]
            if not r:
                return False
            return True
        except IndexError:
            return False
