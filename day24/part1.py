import re
from heapq import heappush
from copy import deepcopy


class Group:
    def __init__(self, faction, units, hp, weaknesses, immunities, ap, power_type, initiative):
        self.faction = faction
        self.units = units
        self.hp = hp
        self.weaknesses = set(weaknesses)
        self.immunities = set(immunities)
        self.ap = ap
        self.power_type = power_type
        self.initiative = initiative
        self.target = None
        self.targeted = False

    def __repr__(self):
        return f'<{self.faction}> ({self.units}, {self.hp})'

    @property
    def effective_power(self):
        return self.units * self.ap

    @property
    def active(self):
        return self.units > 0

    def select_target(self, enemies):
        targets = []            # max heap
        for enemy in enemies:
            if not enemy.active or enemy.targeted:
                continue
            if self.power_type in enemy.weaknesses:
                damage = self.effective_power * 2
            elif self.power_type in enemy.immunities:
                damage = 0
            else:
                damage = self.effective_power

            heappush(targets, (-damage, -enemy.effective_power, -enemy.initiative, enemy))

        if targets:
            # first target is selected, last element is the object itself
            damage, *_, target = targets[0]
            if damage != 0: # don't choose target if no damage can be dealt
                return target

    def take_damage(self, attacker):
        if attacker.power_type in self.weaknesses:
            damage = attacker.effective_power * 2
        elif attacker.power_type in self.immunities:
            damage = 0
        else:
            damage = attacker.effective_power

        self.units -= damage // self.hp

        # self.targeted = False


def target_select_order(g):
    return (g.effective_power, g.initiative)


def attack_order(g):
    return g.initiative


def keep_fighting(immune, infection):
    return (any(group.active for group in immune)
            and any(group.active for group in infection))


def stalemate(immune, infection):
    immune_SOL = False
    infection_SOL = False
    if not any(g.active for g in immune):
        return
    elif not any(g.active for g in infection):
        return
    
    for g1 in immune:
        if g1.active:
            if not all(g1.power_type in g2.immunities for g2 in infection if g2.active):
                break
    else:
        immune_SOL = True

    for g1 in infection:
        if g1.active:
            if not all(g1.power_type in g2.immunities for g2 in immune if g2.active):
                break
    else:
        infection_SOL = True

    return immune_SOL and infection_SOL


def reindeer_simulation(groups, boost=0):
    immune = [group for group in groups if group.faction == 'immune']
    infection = [group for group in groups if group.faction == 'infection']

    for group in immune:
        group.ap += boost

    while keep_fighting(immune, infection):
        # Target selection phase
        for group in sorted(groups, key=target_select_order, reverse=True):
            if group.faction == 'immune':
                target = group.select_target(infection)
            else:
                target = group.select_target(immune)

            if target is not None:
                group.target = target
                target.targeted = True

        # Attacking phase
        for group in sorted(groups, key=attack_order, reverse=True):
            if not group.active or group.target is None:
                continue

            group.target.take_damage(group)

        if boost > 0:
            if not any(group.active for group in immune):
                return

            if stalemate(immune, infection):
                return

        # Reset all groups
        for group in groups:
            group.target = None
            group.targeted = False

    if any(group.active for group in immune):
        units_left = sum(group.units for group in immune if group.active)
    elif any(group.active for group in infection):
        units_left = sum(group.units for group in infection if group.active)

    return units_left


unit_pattern = r'(\d+) units.+with (\d+)'
immune_pattern = r'immune to (.*?)[;)]'
weak_pattern = r'weak to (.*?)[;)]'
attack_pattern = r'(\d+)\s(\w+)\sdamage'
initiative_pattern = r'initiative (\d+)'

groups = []

with open('clue.txt') as f:
    faction = None
    for line in f:
        if line == '\n':
            continue
        if line.startswith('Immune System'):
            faction = 'immune'
            continue
        elif line.startswith('Infection'):
            faction = 'infection'
            continue

        units, hp = map(int, re.search(unit_pattern, line).groups())
        weak = re.search(weak_pattern, line)
        if weak:
            weaknesses = weak.group(1).split(', ')
        else:
            weaknesses = []
        immune = re.search(immune_pattern, line)
        if immune:
            immunities = immune.group(1).split(', ')
        else:
            immunities = []
        attack = re.search(attack_pattern, line)
        ap = int(attack.group(1))
        power_type = attack.group(2)
        initiative = int(re.search(initiative_pattern, line).group(1))

        groups.append(Group(faction, units, hp, weaknesses, immunities, ap, power_type, initiative))

units_left = reindeer_simulation(deepcopy(groups))

print('Part 1:', units_left)

boost = 1
while True:
    group_copy = deepcopy(groups)
    units_left = reindeer_simulation(group_copy, boost)
    if units_left is None:
        boost += 1
    else:
        break

print('Part 2:', units_left)
print(f'Boost: {boost}')
