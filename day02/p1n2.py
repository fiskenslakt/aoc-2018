from collections import Counter
from itertools import combinations


with open('clue.txt') as f:
    box_ids = f.read().splitlines()

two = three = 0

for box in box_ids:
    letter_freq = Counter(box)
    if 2 in letter_freq.values():
        two += 1
    if 3 in letter_freq.values():
        three += 1

print('Part 1:', two*three)

for box1, box2 in combinations(box_ids, 2):
    diff = 0
    for c1, c2 in zip(box1, box2):
        if c1 != c2:
            diff += 1
    if diff == 1:
        print('Part 2:', ''.join([c for c in box1 if c in box2]))
        break
