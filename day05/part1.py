with open('clue.txt') as f:
    polymer = f.read().strip()

skip_index = set()
i = 0

while i <= len(polymer)-3:
    while i in skip_index and i <= len(polymer)-3:
        i += 1

    j = i+1
    while j in skip_index and j <= len(polymer)-2:
        j += 1

    if polymer[i].swapcase() == polymer[j]:
        skip_index.add(i)
        skip_index.add(j)
        while i >= 1 and i in skip_index:
            i -= 1
    else:
        i += 1

print(len(polymer) - len(skip_index))
