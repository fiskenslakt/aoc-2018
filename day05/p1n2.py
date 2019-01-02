import string


def react(polymer, skip_letter=None):
    stack = []

    for unit in polymer:
        if unit.lower() == skip_letter:
            continue

        if stack and unit.swapcase() == stack[-1]:
            stack.pop()
        else:
            stack.append(unit)

    return ''.join(stack)


with open('clue.txt') as f:
    polymer = f.read().strip()

polymer = react(polymer)

print(f'Part 1: {len(polymer)}')

polymer_lengths = []

for letter in string.ascii_lowercase:
    polymer_lengths.append(len(react(polymer, letter)))

best_len = min(polymer_lengths)

print(f'Part 2: {best_len}')
