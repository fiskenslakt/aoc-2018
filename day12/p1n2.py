import heapq

with open('clue.txt') as f:
    raw_data = f.read().splitlines()

pots = [i for i, pot in enumerate(raw_data[0].split()[-1]) if pot == '#']
heapq.heapify(pots)

notes = set()
test = []
for note in raw_data[2:]:
    note = note.split(' => ')
    if note[1] == '#':
        key = ''
        for pot in note[0]:
            if pot == '#':
                key += '1'
            else:
                key += '0'
        notes.add(int(key, 2))
        test.append(int(key, 2))

for gen in range(20):
    # print('gen:',gen)
    all_pots = []
    smallest_pot = min(pots)

    for i in range(min(pots)-4, max(pots)+5):
        if i in pots:
            all_pots.append('1')
        else:
            all_pots.append('0')

    pots = []

    for i in range(len(all_pots)-5):
        if int(''.join(all_pots[i:i+5]), 2) in notes:
            heapq.heappush(pots, smallest_pot-2+i)

    # print(min(pots), max(pots))

print('Part 1:', sum(pots))

billion_min = 50000000000 - 100
billion_max = billion_min + 193
print('Part 2:',sum(range(billion_min, billion_max+1)))
