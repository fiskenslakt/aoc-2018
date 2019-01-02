from pprint import pprint

def dist(pt1, pt2):
    # print(pt1)
    x1, y1, z1, t1 = pt1
    x2, y2, z2, t2 = pt2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dz = abs(z1 - z2)
    dt = abs(t1 - t2)

    return sum((dx, dy, dz, dt))
        

pts = [
    (1,-1,0,1),
    (2,0,-1,0),
    (3,2,-1,0),
    (0,0,3,1),
    (0,0,-1,-1),
    (2,3,-2,0),
    (-2,2,0,0),
    (2,-2,0,-1),
    (1,-1,0,-1),
    (3,2,0,2),
]

with open('nomad.txt') as f:
    pts = []
    for line in f:
        pts.append(tuple(map(int, line.split(','))))

points = {}
ignore = set()
for pt1 in pts:
    if pt1 in ignore:
        continue
    if pt1 not in points:
        points[pt1] = set()

    for pt2 in pts:
        if pt1 == pt2:
            continue
        if dist(pt1, pt2) <= 3:
            points[pt1].add(pt2)
            ignore.add(pt2)

keys = sorted(points.keys())
constellations = 0
branches = {}
looked_at = set()
ignore = set()

for k1 in keys:
    if k1 in ignore:
        continue
    constellations += 1
    # branches[k1] = set()
    for k2 in keys:
        for pt in points[k1]:
            if pt in points[k2]:
                ignore.add(k2)

print(constellations)

# for k1 in keys:
#     unique = True
#     # branches[k1] = set()
#     if k1 in branches:
#         # constellations += 1
#         continue
#     # else:
#     #     continue
#         # ignore.add(k1)
#     if constellations == 0:
#         if len(points[k1]) > 0:
#             constellations += 1
#             continue
#     # if len(points[k1]) == 0:
#     #     constellations += 1
#     #     continue
        
#     for pt in points[k1]:
#         for k2 in keys:
#             # if k2 in ignore:
#             if k2 == k1:
#                 continue
#             if pt in points[k2]:
#                 unique = False
#                 branches.add(k2)
#                 # if k1 not in branches:
#                 #     branches[k1] = set()
#                 # branches[k1].add(k2)
#                 # break
#         if not unique:
#             break
#     else:
#         constellations += 1

#     if k1 not in branches:
#         constellations += 1

# print(f'Part 1: {constellations}')

# # 468 Too high
# # 356 Too low
# # 229 Too low
