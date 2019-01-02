with open('clue.txt') as f:
    raw_data = f.read().splitlines()

# initial_state = [1 if pot == '#' else 0 for pot in raw_data[0].split()[-1]]
initial_state = list(raw_data[0].split()[-1])
initial_len = len(initial_state)
pots = ['.']*10_000 + initial_state + ['.']*10_000

notes = {}

for note in raw_data[2:]:
    note = note.split(' => ')
    notes[tuple(note[0])] = note[1]

generations = []
# for gen in range(20):
for gen in range(50_000_000_000):
# for gen in range(1196):
    # print(gen)
    new_pots = set()

    for i in range(len(pots)):
        if notes.get(tuple(pots[i:i+5])) == '#':
            new_pots.add(i+2)

    pots = ['#' if i in new_pots else '.' for i in range(len(pots))]
    if new_pots in generations:
        print(gen)

    generations.append(new_pots)

    # print(gen, pots)
print(pots)

plants = 0
for i, pot in enumerate(pots):
    i -= 50
    if pot == '#':
        plants += i

print('plants left:', plants)
