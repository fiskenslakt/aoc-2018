def manhattan_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

with open('clue.txt') as f:
    coords = [tuple(map(int,coord.split(', '))) for coord in f.read().splitlines()]

x_min = min(x for x, _ in coords)
x_max = max(x for x, _ in coords)
y_min = min(y for _, y in coords)
y_max = max(y for _, y in coords)

infinite_coords = set()

for x_border in (x_min, x_max):
    for y in range(y_min, y_max+1):
        closest = None
        for coord in coords:
            dist = manhattan_distance(coord, (x_border, y))
            if closest is None:
                closest = (coord, dist)
            elif dist < closest[1]:
                closest = (coord, dist)
                
        infinite_coords.add(closest[0])

for y_border in (y_min, y_max):
    for x in range(x_min, x_max+1):
        closest = None
        for coord in coords:
            dist = manhattan_distance(coord, (x, y_border))
            if closest is None:
                closest = (coord, dist)
            elif dist < closest[1]:
                closest = (coord, dist)
                
        infinite_coords.add(closest[0])        

finite_coords = list(set(coords) - infinite_coords)

coord_areas = {}

for coord in finite_coords:
    if coord not in coord_areas:
        coord_areas[coord] = 1

    x, y = coord

    for i in range(y_min, y_max+1):
        for j in range(x_min, x_max+1):
            if (j,i) in coords:
                continue

            dist_from_coord = manhattan_distance(coord, (j,i))

            for coord2 in coords:
                if coord == coord2:
                    continue
                if dist_from_coord >= manhattan_distance(coord2, (j,i)):
                    break
            else:
                coord_areas[coord] += 1

print(coord_areas[max(coord_areas, key=coord_areas.get)])
