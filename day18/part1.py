import numpy as np


def check_adjacent(area, x, y):
    y_max, x_max = area.shape
    trees = 0
    lumber = 0

    for i, j in [(-1,-1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
        if 0 <= x+i < x_max and 0 <= y+j < y_max:
            if area[y+j, x+i] == '|':
                trees += 1
            elif area[y+j, x+i] == '#':
                lumber += 1

    return trees, lumber


with open('clue.txt') as f:
    acres_raw = []
    for line in f:
        acres_raw.append(list(line.strip()))

area = np.array(acres_raw)
y_max, x_max = area.shape

# scores = set()
# found = False
for minute in range(1, 1_000_000_000):
    changes = {}

    # for col in area:
    #     print(''.join(col),end='')
    #     print()

    for y in range(y_max):
        for x in range(x_max):
            if area[y, x] == '.' and check_adjacent(area, x, y)[0] >= 3:
                changes[(x, y)] = '|'
            elif area[y, x] == '|' and check_adjacent(area, x, y)[1] >= 3:
                changes[(x, y)] = '#'
            elif area[y, x] == '#':
                if check_adjacent(area, x, y)[0] >= 1 and check_adjacent(area, x, y)[1] >= 1:
                    changes[(x, y)] = '#'
                else:
                    changes[(x, y)] = '.'

    for (x,y), change in changes.items():
        area[y, x] = change

    if minute == 10:
        trees = 0
        lumber = 0

        for row in area:
            for col in row:
                if col == '|':
                    trees += 1
                elif col == '#':
                    lumber += 1
        print('Part 1:', trees*lumber)
    elif minute < 552:
        continue
    elif (1_000_000_000 - minute) % 28 == 0:
        break

trees = 0
lumber = 0

for row in area:
    for col in row:
        if col == '|':
            trees += 1
        elif col == '#':
            lumber += 1

print('Part 2:', trees*lumber)
