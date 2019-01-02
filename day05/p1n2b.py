import string


with open('clue.txt') as f:
    polymer = f.read().strip()


def react(polymer, skip_letter=None):
    stack = []

    for unit in polymer:
        if unit.lower() == skip_letter:
            continue

        if stack and unit.swapcase() == stack[-1]:
            stack.pop()
        else:
            stack.append(unit)

    return len(stack)


print(f'Part 1: {react(polymer)}')

polymer_lengths = []

for letter in string.ascii_lowercase:
    polymer_lengths.append(react(polymer, letter))

print(f'Part 2: {min(polymer_lengths)}')
