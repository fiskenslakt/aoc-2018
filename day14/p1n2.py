target = 290431
target2 = [int(i) for i in str(target)]

recipes = [3, 7]
elf1 = 0
elf2 = 1

part1 = True

while True:
    if len(recipes) >= target+10 and part1:
        print('Part 1:', ''.join(map(str,recipes[-10:])))
        part1 = False

    new_recipe = recipes[elf1] + recipes[elf2]
    recipes.extend(divmod(new_recipe, 10) if new_recipe >= 10 else (new_recipe,))

    if recipes[-6:] == target2 or recipes[-7:-1] == target2:
        if recipes[-6] == target2[-6]:
            print('Part 2:', len(recipes) - 6)
        else:
            print('Part 2:', len(recipes) - 7)
        break

    elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
    elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
