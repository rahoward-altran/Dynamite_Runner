import random

EMPTY_DYNAMITE = 0
FULL_DYNAMITE = 100
DYNAMITE_THRESHOLD = 10
CONFIDENCE_THRESHOLD = 5
NO_CONFIDENCE = 0

class SmartBot:
    def __init__(self):
        # todo: reconsider? always not use at least one dynamite so opponent's logic can't be certain I won't use it
        self.dynamite_left = FULL_DYNAMITE -1
        self.opponent_dynamite_left = FULL_DYNAMITE
        self.opponent_move_usage = {'W': 0, 'D': 0, 'R': 0, 'S': 0, 'P': 0}
        self.opponent_fav_move = ("", 0)
        self.confidence = 0  # finite state of faith in opponents fav move
        # self.opponents_last_10 = ""
        self.win_map = {
            "R": {
                "R": "D",
                "P": "L",
                "S": "W",
                "D": "L",
                "W": "W"
            },
            "P": {
                "R": "W",
                "P": "D",
                "S": "L",
                "D": "L",
                "W": "W"
            },
            "S": {
                "R": "L",
                "P": "W",
                "S": "D",
                "D": "L",
                "W": "W"
            },
            "D": {
                "R": "W",
                "P": "W",
                "S": "W",
                "D": "D",
                "W": "L"
            },
            "W": {
                "R": "L",
                "P": "L",
                "S": "L",
                "D": "W",
                "W": "D"
            }
        }

    def make_move(self, gamestate):
        self.update_info_on_opponent(gamestate['rounds'])

        # if confident with fav move play opposite
        # else random - if no dynamite don't play water
        if self.confidence >= CONFIDENCE_THRESHOLD:
            return self.beat_their_favourite()
        else:
            return self.random_attack()

    def update_info_on_opponent(self, rounds_list):
        try:
            last_round = rounds_list[-1]
        except IndexError:
            # round list is empty
            return

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

        self.update_opponent_fav_move()

    def update_opponent_fav_move(self):
        most_used_move = self.opponent_fav_move[0]
        most_used_move_value = self.opponent_fav_move[1]

        # if they have used all there dynamite then it will never be their favourite move again
        # remove from list so don't risk using water after last dynamite has been played
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
        self.opponent_fav_move = (most_used_move, most_used_move_value)

    def random_attack(self):
        # low confidence - higher use of dynamite if available
        if self.dynamite_left == EMPTY_DYNAMITE:
            move = random.randint(1, 3)
        else:
            move = random.randint(1, 20)
        # Never uses water when not confident. risks are too high
        # todo:  reconsider
        if move == 0:
            return "W"
        elif move == 1:
            return "R"
        elif move == 2:
            return "P"
        elif move == 3:
            return "S"
        elif move >= 4:
            self.dynamite_left -= 1
            return "D"

    def beat_their_favourite(self):
        winning_moves = []
        for move, result in self.win_map[self.opponent_fav_move[0]].items():
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








