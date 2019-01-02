from itertools import combinations

with open('clue.txt') as f:
    claims_raw = f.read().splitlines()

claims = []

for claim in claims_raw:
    pos, area = claim.split(':')
    a, b = area.strip().split('x')
    x, y = pos.split()[-1].split(',')

    claims.append(((int(x), int(y)), (int(a), int(b))))

# claims = [
#     ((1,3), (4,4)),             # (4, 6)
#     ((2,1), (5,4)),             # (6, 4)
#     # ((3,1), (4,4)),    
#     # ((5,5), (2,2)),
#     # ((3,3), (3,3))
#     # ((4,1), (3,4))
# ]

inches = 0
# overlaps = []

for a, b in combinations(claims, 2):
    (ax, ay), (aw, ah) = a
    (bx, by), (bw, bh) = b

    Ax = ax + aw - 1
    Ay = ay + ah - 1
    Bx = bx + bw - 1
    By = by + bh - 1

    x_overlap = min(Ax, Bx) - max(ax, bx) + 1
    y_overlap = min(Ay, By) - max(ay, by) + 1

    if x_overlap > 0 and y_overlap > 0:
        inches += x_overlap * y_overlap
    
    # if x_overlap > 0:
    #     inches += x_overlap
    #     # overlaps.append(((), ()))
    # if y_overlap > 0:
    #     inches += y_overlap

print(inches)
