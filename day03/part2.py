with open('clue.txt') as f:
    claims_raw = f.read().splitlines()

claims = []

for claim in claims_raw:
    pos, area = claim.split(':')
    a, b = area.strip().split('x')
    x, y = pos.split()[-1].split(',')
    ID = pos.split()[0][1:]

    claims.append((ID, (int(x), int(y)), (int(a), int(b))))

cut_points = {}

for ID, (x, y), (w, h) in claims:
    for Y in range(y, y+h):
        for X in range(x, x+w):
            if (X, Y) not in cut_points:
                cut_points[(X,Y)] = [ID]
            else:
                cut_points[(X,Y)].append(ID)

checked_ids = set()                
for v in cut_points.values():
    if len(v) == 1 and v[0] not in checked_ids:
        checked_ids.add(v[0])
        for overlap in cut_points.values():
            if len(overlap) > 1:
                if v[0] in overlap:
                    break
            else:
                continue
        else:
            print(v[0])
            break
