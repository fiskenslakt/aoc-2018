from itertools import combinations

with open('clue.txt') as f:
    coords = [tuple(coord.split(', ')) for coord in f.read().splitlines()]

x_min = 100
x_max = 100
y_min = 100
y_max = 100

for x, y in coords:
    x = int(x)
    y = int(x)

    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x

    if y < y_min:
        y_min = y
    if y > y_max:
        y_max = y

# print(x_min, x_max, y_min, y_max)

coord_dist = {}

for c1 in coords:
    if c1[0] == x_min:
        continue
    if c1[0] == x_max:
        continue
    if c1[1] == y_min:
        continue
    if c1[1] == y_max:
        continue

    if c1 not in coord_dist:
        coord_dist[c1] = 0

    closest = None
    for c2 in coords:
        if c1 == c2:
            continue
        dist = abs(int(c1[0]) - int(c2[0])) + abs(int(c1[1]) - int(c2[1]))
        if closest is None:
            closest = dist
        elif dist < closest:
            closest = dist

    coord_dist[c1] += closest

print(max(coord_dist, key=coord_dist.get))
