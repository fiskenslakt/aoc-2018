import re
import numpy as np


class Water:
    def __init__(self, x, y, ground):
        self.x = x
        self.y = y
        self.ground = ground
        self.y_max, self.x_max = self.ground.shape
        self.y_max -= 1
        self.water_tiles = set()

        self.fall(self.x, self.y)

    @property
    def amount(self):
        return len(self.water_tiles)

    @property
    def retained(self):
        tiles = 0
        for row in self.ground:
            for col in row:
                if col == '~':
                    tiles += 1
        return tiles

    def can_fall(self, x, y):
        if y == self.y_max:
            return False
        
        if self.ground[y+1,x] == '#':
            return False
        if (x, y+1) in self.water_tiles:
            return False

        return True

    def can_spread_left(self, x, y):
        if self.can_fall(x,y):
            return False
        
        if x == 0 or y == self.y_max:
            return False

        if self.ground[y+1,x] == '|':
            return False
        
        if self.ground[y,x-1] == '#':
            return False

        if self.ground[y,x-1] == '~':
            return False

        return True

    def can_spread_right(self, x, y):
        if self.can_fall(x, y):
            return False
        
        if x == self.x_max or y == self.y_max:
            return False

        if self.ground[y+1,x] == '|':
            return False

        if self.ground[y,x+1] == '#':
            return False

        if self.ground[y,x+1] == '~':
            return False

        return True

    def can_spread(self, x, y):
        if self.can_spread_left(x, y):
            return True
        if self.can_spread_right(x, y):
            return True

    # def can_flow(self, x, y):
    #     return self.can_spread(x, y) or self.can_fall(x, y)

    def fall(self, x, y):
        last_flow = [(x,y)]

        while self.can_fall(x, y):
            y += 1
            self.water_tiles.add((x, y))
            self.ground[y, x] = '|'
            last_flow.append((x,y))

        if y == self.y_max or self.ground[y+1,x] == '|':
            last_flow.pop()
            return

        while last_flow:
            fill_left = self.spread_left(x, y)
            fill_right = self.spread_right(x, y)

            if fill_left and fill_right and y != self.y_max:
                self.ground[y,x] = '~'
                fill_x = x
                while self.ground[y,fill_x-1] != '#':
                    fill_x -= 1
                    self.ground[y, fill_x] = '~'

                fill_x = x
                while self.ground[y,fill_x+1] != '#':
                    fill_x += 1
                    self.ground[y, fill_x] = '~'

            if last_flow:
                x, y = last_flow.pop()

    def spread_left(self, x, y):
        while self.can_spread_left(x, y):
            x -= 1
            self.water_tiles.add((x, y))
            self.ground[y, x] = '|'
            
            if self.can_fall(x, y):
                self.fall(x, y)
        else:
            if self.ground[y,x-1] == '#':
                return True

    def spread_right(self, x, y):
        while self.can_spread_right(x, y):
            x += 1
            self.water_tiles.add((x, y))
            self.ground[y, x] = '|'

            if self.can_fall(x, y):
                self.fall(x, y)
        else:
            if self.ground[y,x+1] == '#':
                return True
            
    def display(self):
        for i, row in enumerate(self.ground):
            print(''.join(row)+f'{i}', end='')
            print()


with open('clue.txt') as f:
    clay_raw = f.read().splitlines()

# clay_raw = [
#     'x=495, y=2..7',
#     'y=7, x=495..501',
#     'x=501, y=3..7',
#     'x=498, y=2..4',
#     'x=506, y=1..2',
#     'x=498, y=10..13',
#     'x=504, y=10..13',
#     'y=13, x=498..504',
# ]

x_pattern = r'x=(\d+)\.{0,2}(\d+)?'
y_pattern = r'y=(\d+)\.{0,2}(\d+)?'

x_values = []
y_values = []

for line in clay_raw:
    x_values.extend(re.findall(x_pattern, line))
    y_values.extend(re.findall(y_pattern, line))

x_min = min(int(v) for t in x_values for v in t if v) - 1
x_max = max(int(v) for t in x_values for v in t if v) + 1
y_min = min(int(v) for t in y_values for v in t if v)
y_max = max(int(v) for t in y_values for v in t if v)

offset = x_min

ground = np.empty((y_max+1, x_max-offset), dtype=str)
ground[:] = '.'

for x, y in zip(x_values, y_values):
    if not x[1]:
        x = int(x[0]) - offset
        for i in range(int(y[0]), int(y[1])+1):
            ground[i,x] = '#'

    elif not y[1]:
        y = int(y[0])
        for i in range(int(x[0])-offset, int(x[1])-offset+1):
            ground[y,i] = '#'

spring = [500-offset, y_min-1]
ground[spring[1],spring[0]] = '+'

water = Water(spring[0], spring[1], ground)

print('Part 1:',water.amount)
print('Part 2:',water.retained)
