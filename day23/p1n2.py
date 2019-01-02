import re
from heapq import heappush, heappop


class Bot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def signal_intersects(self, x1, y1, z1, x2, y2, z2):
        dist = 0

        if self.x < x1:
            dist += x1 - self.x
        elif self.x > x2:
            dist += self.x - x2

        if self.y < y1:
            dist += y1 - self.y
        elif self.y > y2:
            dist += self.y - y2

        if self.z < z1:
            dist += z1 - self.z
        elif self.z > z2:
            dist += self.z - z2

        return dist <= self.r


class NanoBots:
    def __init__(self, bot_data):
        with open(bot_data) as f:
            self.bots = [Bot(*map(int, re.findall(r'-?\d+', line))) for line in f]

        x_min = min(b.x for b in self.bots)
        x_max = max(b.x for b in self.bots)
        y_min = min(b.y for b in self.bots)
        y_max = max(b.y for b in self.bots)
        z_min = min(b.z for b in self.bots)
        z_max = max(b.z for b in self.bots)

        self.x_min, self.y_min, self.z_min = x_min, y_min, z_min

        self.square = 1
        while self.square < max(x_max - x_min, y_max - y_min, z_max - z_min):
            self.square *= 2
            
        self.queue = []

    def add_point(self, x1, y1, z1):
        x2 = x1 + self.square - 1
        y2 = y1 + self.square - 1
        z2 = z1 + self.square - 1

        in_range = 0

        for bot in self.bots:
            if bot.signal_intersects(x1, y1, z1, x2, y2, z2):
                in_range += 1

        if in_range > 0:
            corner = (min(abs(x1), abs(x2)), min(abs(y1), abs(y2)), min(abs(z1), abs(z2)))
            dist = sum(corner)
            heappush(self.queue, (-in_range, dist, self.square, x1, y1, z1))

    def best_bot(self):
        in_range = 0
        big_bot = None
        for bot in self.bots:
            if big_bot is None:
                big_bot = bot
            elif bot.r > big_bot.r:
                big_bot = bot

        for bot in self.bots:
            if big_bot - bot <= big_bot.r:
                in_range += 1

        print(f'Part 1: {in_range}')

    def best_point(self):
        self.add_point(self.x_min, self.y_min, self.z_min)

        while self.queue:
            in_range, dist, self.square, x, y, z = heappop(self.queue)
            
            if self.square == 1:
                print(f'Part 2: {dist}')
                break

            self.square //= 2
            # 8 subdivisions of previous box
            self.add_point(x, y, z)
            self.add_point(x+self.square, y, z)
            self.add_point(x, y+self.square, z)
            self.add_point(x, y, z+self.square)
            self.add_point(x+self.square, y+self.square, z)
            self.add_point(x, y+self.square, z+self.square)
            self.add_point(x+self.square, y, z+self.square)
            self.add_point(x+self.square, y+self.square, z+self.square)
                

nano_bots = NanoBots('clue.txt')
nano_bots.best_bot()
nano_bots.best_point()
