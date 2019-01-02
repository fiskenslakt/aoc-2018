import re


with open('clue.txt') as f:
    claims_raw = f.read().splitlines()

claims = []

for claim in claims_raw:
    ID, x, y, w, h = re.findall(r'\d+', claim)
    claims.append((ID, (int(x), int(y)), (int(w), int(h))))

cut_points = {}
overlaps = set()
no_overlap = set()

for ID, (x,y), (w,h) in claims:
    for Y in range(y, y+h):
        for X in range(x, x+w):
            if (X,Y) not in cut_points:
                cut_points[(X,Y)] = [ID]
                if ID not in overlaps:
                    no_overlap.add(ID)
            else:
                cut_points[(X,Y)].append(ID)
                overlaps.add(ID)
                for overlap in cut_points[(X,Y)]:
                    no_overlap.discard(overlap)

inches_that_overlap = sum(1 for inch in cut_points.values() if len(inch) > 1)
print(f'Part 1: {inches_that_overlap}')
print(f'Part 2:', no_overlap.pop())
