with open('clue.txt') as f:
    claims_raw = f.read().splitlines()

claims = []

for claim in claims_raw:
    pos, area = claim.split(':')
    a, b = area.strip().split('x')
    x, y = pos.split()[-1].split(',')

    claims.append(((int(x), int(y)), (int(a), int(b))))

cut_points = {}

for (x, y), (w, h) in claims:
    for Y in range(y, y+h):
        for X in range(x, x+w):
            if (X, Y) not in cut_points:
                cut_points[(X, Y)] = 1
            else:
                cut_points[(X, Y)] += 1

print(sum(1 for inches in cut_points.values() if inches > 1))
