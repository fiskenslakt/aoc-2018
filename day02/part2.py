with open('clue.txt') as f:
    box_ids = f.read().splitlines()

for idx, i in enumerate(box_ids):
    for j in box_ids[idx:]:
        diff = 0
        for a, b in zip(i,j):
            if a != b:
                diff += 1

        if diff == 1:
            print(''.join([char for char in i if char in j]))
            raise SystemExit
