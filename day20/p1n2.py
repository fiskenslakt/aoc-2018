import networkx as nx


facility = nx.Graph()

cardinal = {
    'N': 1j,
    'S': -1j,
    'E': 1,
    'W': -1,
}

with open('clue.txt') as f:
    regex = f.read().strip('^$')

cur_pos = 0
start_stack = []
cur_start = 0

for d in regex:
    if d.isalpha():
        new_pos = cardinal[d]
        facility.add_edge(cur_pos, cur_pos + new_pos)
        cur_pos += new_pos
    elif d == '(':
        start_stack.append(cur_start)
        cur_start = cur_pos
    elif d == '|':
        cur_pos = cur_start
    elif d == ')':
        cur_start = start_stack.pop()

path_lengths = nx.algorithms.shortest_path_length(facility, 0)

print('Part 1:', max(path_lengths.values()))
print('Part 2:', sum(1 for path in path_lengths.values() if path >= 1_000))
