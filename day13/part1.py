from itertools import combinations
from collections import deque
import numpy as np


class Track:
    with open('clue.txt') as f:
        tracks = np.array([[track for track in line] for line in f.read().splitlines()])


class Cart(Track):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.turns = deque(['left', 'straight', 'right'])

    def _next_direction(self):
        if self.turns[0] == 'straight':
            d = self.facing
        elif self.turns[0] == 'left':
            if self.facing == 'left':
                d = 'down'
            elif self.facing == 'up':
                d = 'left'
            elif self.facing == 'right':
                d = 'up'
            else:
                d = 'right'
        elif self.turns[0] == 'right':
            if self.facing == 'left':
                d = 'up'
            elif self.facing == 'up':
                d = 'right'
            elif self.facing == 'right':
                d = 'down'
            else:
                d = 'left'
        self.turns.rotate(-1)
        return d

    def _move_right(self):
        track = self.tracks[self.y,self.x+1]
        if track == '+':
            self.facing = self._next_direction()
        elif track == '/':
            self.facing = 'up'
        elif track == '\\':
            self.facing = 'down'
        self.x += 1

    def _move_left(self):
        track = self.tracks[self.y,self.x-1]
        if track == '+':
            self.facing = self._next_direction()
        elif track == '/':
            self.facing = 'down'
        elif track == '\\':
            self.facing = 'up'
        self.x -= 1

    def _move_up(self):
        track = self.tracks[self.y-1,self.x]
        if track == '+':
            self.facing = self._next_direction()
        elif track == '/':
            self.facing = 'right'
        elif track == '\\':
            self.facing = 'left'
        self.y -= 1

    def _move_down(self):
        track = self.tracks[self.y+1,self.x]
        if track == '+':
            self.facing = self._next_direction()
        elif track == '/':
            self.facing = 'left'
        elif track == '\\':
            self.facing = 'right'
        self.y += 1

    def move(self):
        # print(self.x,self.y)
        if self.facing == 'right':
            self._move_right()
        elif self.facing == 'left':
            self._move_left()
        elif self.facing == 'up':
            self._move_up()
        else:
            self._move_down()


def collision_found(carts):
    all_carts = len(carts)
    carts_left = len(set((cart.x, cart.y) for cart in carts))
    return carts_left < all_carts


def all_collisions(carts):
    collisions = set()
    for cart1, cart2 in combinations(carts, 2):
        cart1_pos = (cart1.x, cart1.y)
        cart2_pos = (cart2.x, cart2.y)
        if cart1_pos == cart2_pos:
            collisions.add(cart1)
            collisions.add(cart2)
    return collisions

def get_cart_order(cart):
    return (cart.y, cart.x)


tracks = Track().tracks

directions = {
    '>': 'right',
    '<': 'left',
    'v': 'down',
    '^': 'up'
}

carts = []

rows, cols = tracks.shape

for row in range(rows):
    for col in range(cols):
        if tracks[row,col] in directions:
            carts.append(Cart(col, row, directions[tracks[row,col]]))

carts2 = []

for row in range(rows):
    for col in range(cols):
        if tracks[row,col] in directions:
            carts2.append(Cart(col, row, directions[tracks[row,col]]))
            
collision = False
while not collision:
    for cart in sorted(carts, key=get_cart_order):
        cart.move()
        if collision_found(carts):
            collision = True
            break

for cart1, cart2 in combinations(carts, 2):
    cart1 = (cart1.x, cart1.y)
    cart2 = (cart2.x, cart2.y)
    if cart1 == cart2:
        print('Part 1:',cart1)

while len(carts2) > 1:
    for cart in sorted(carts2.copy(), key=get_cart_order):
        cart.move()
        if collision_found(carts2):
            for cart in all_collisions(carts2):
                carts2.remove(cart)

last_cart = carts2.pop()
print(f'Part 2: {last_cart.x,last_cart.y}')
