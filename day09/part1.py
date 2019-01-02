from collections import deque
from itertools import cycle


class Circle:
    def __init__(self, player_amount, last_marble):
        self.player_amount = player_amount
        self.last_marble = last_marble
        self.scores = [0] * player_amount
        self.players = deque(range(player_amount, 0, -1))
        self.circle = deque([0])
        self.cur_marble_pos = 0
        self.cur_marble_value = 1

    def __str__(self):
        return f'[{self.player}] {self.circle} {self.cur_marble_pos}'

    @property
    def player(self):
        return self.players[-1]

    def normal_turn(self):
        if len(self.circle) == 1:
            self.circle.append(self.cur_marble_value)
            self.cur_marble_pos = len(self.circle)-1
            self.cur_marble_value += 1
            self.players.rotate()
        else:
            circle_cycle = cycle(self.circle)
            for _ in range(self.cur_marble_pos+2):
                marble_to_insert = next(circle_cycle)
                # print(marble_to_insert, self.circle.index(marble_to_insert))

            self.cur_marble_pos = self.circle.index(marble_to_insert)+1
            self.circle.insert(self.cur_marble_pos, self.cur_marble_value)
            self.cur_marble_value += 1
            self.players.rotate()

    def points_turn(self):
        other_marble = self.circle[self.cur_marble_pos-7]
        print('cur marble', self.cur_marble_value)
        print('last marble', self.circle[self.cur_marble_pos])
        print('other marble', other_marble)
        self.scores[self.player-1] += self.cur_marble_value + other_marble
        self.circle.remove(other_marble)
        self.cur_marble_pos = self.circle.index(self.circle[self.cur_marble_pos-7])
        self.cur_marble_value += 1
        self.players.rotate()

circle = Circle(10, 100)

while circle.cur_marble_value < circle.last_marble:
    print(circle)
    if circle.cur_marble_value % 23 == 0:
        # print(circle)

        # if circle.cur_marble_value == 23*10:
        #     break
        
        circle.points_turn()
    else:
        circle.normal_turn()

# print(max(circle.scores))
