from collections import Counter

with open('clue.txt') as f:
    box_ids = f.read().splitlines()

two = 0
three = 0
    
for box in box_ids:
    if 2 in Counter(box).values():
        two += 1
    if 3 in Counter(box).values():
        three += 1

print(two*three)        
