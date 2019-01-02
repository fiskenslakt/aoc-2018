def manhattan_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

with open('clue.txt') as f:
    coords = [tuple(map(int,coord.split(', '))) for coord in f.read().splitlines()]

x_min = min(x for x, _ in coords)
x_max = max(x for x, _ in coords)
y_min = min(y for _, y in coords)
y_max = max(y for _, y in coords)

region = 0

for x in range(x_min, x_max+1):
    for y in range(y_min, y_max+1):
        dist_all_coords = 0
        for coord in coords:
            dist_all_coords +=  manhattan_distance((x,y), (coord))
            
        if dist_all_coords < 10_000:
            region += 1

print(region)
