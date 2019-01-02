import networkx as nx
from functools import lru_cache
from itertools import combinations


@lru_cache(None)
def geological_index(x, y):
    if x == y == 0:
        return 0
    elif x == 12 and y == 763:
        return 0
    elif x > 0 and y == 0:
        return x * 16807
    elif y > 0 and x == 0:
        return y * 48271
    else:
        return erosion_level(geological_index(x-1, y)) * erosion_level(geological_index(x, y-1))

    
def erosion_level(index):
    return (index + 7_740) % 20183


def usable_tools(risk):
    if risk == 0: return (1, 2)
    if risk == 1: return (0, 1)
    if risk == 2: return (0, 2)


# depth = 7_740
# tx, ty = (12,763)
# MOD = 20183
risk = 0

for row in range(764):
    for col in range(13):
        risk += erosion_level(geological_index(col, row)) % 3

print('Part 1:', risk)

G = nx.Graph()

for row in range(764+100):
    for col in range(13+100):
        risk = erosion_level(geological_index(col, row)) % 3
        usable = usable_tools(risk)
        for t1, t2 in combinations(usable, 2):
            G.add_edge((col, row, t1), (col, row, t2), weight=7)

for y in range(764+100):
    for x in range(13+100):
        for i, j in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if not 0 <= x+i <= 12+100:
                continue
            if not 0 <= y+j <= 763+100:
                continue

            risk_from = erosion_level(geological_index(x, y)) % 3
            risk_to = erosion_level(geological_index(x+i, y+j)) % 3

            usable = set(usable_tools(risk_from)) & set(usable_tools(risk_to))
            for tool in usable:
                G.add_edge((x,y,tool), (x+i,y+j,tool), weight=1)

minutes = nx.dijkstra_path_length(G, (0,0,2), (12,763,2))
print('Part 2:', minutes)
