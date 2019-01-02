class Constellation:
    def __init__(self, pt=None, chain=None):
        if chain is None:
            self.chain = set([pt])
        else:
            self.chain = chain

    def __contains__(self, pt):
        return pt in self.chain

    def __add__(self, other):
        self.chain.update(other.chain)

    def should_merge(self, other):
        return len(self.chain & other.chain)

    def add_pt(self, pt):
        self.chain.add(pt)

    def belongs(self, pt1):
        for pt2 in self.chain:
            if self.dist(pt1, pt2) <= 3:
                return True

    def dist(self, pt1, pt2):
        x1, y1, z1, t1 = pt1
        x2, y2, z2, t2 = pt2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        dz = abs(z1 - z2)
        dt = abs(t1 - t2)

        return sum((dx, dy, dz, dt))


with open('clue.txt') as f:
    pts = []
    for line in f:
        pts.append(tuple(map(int, line.split(','))))

constellations = set()

for pt in sorted(pts):
    unique = True

    for constellation in constellations:
        if pt in constellation:
            unique = False
            continue
        if constellation.belongs(pt):
            unique = False
            constellation.add_pt(pt)

    if unique:
        constellations.add(Constellation(pt=pt))

c = constellations.copy()
final = []

for c1 in constellations:
    if c1 not in c:
        continue
    final.append(c.pop())
    while True:
        merges = False
        for c2 in constellations:
            if c2 not in c:
                continue
            if final[-1].should_merge(c2):
                merges = True
                c.discard(c2)
                final[-1] + c2
        if not merges:
            break

print('Part 1:', len(final))
