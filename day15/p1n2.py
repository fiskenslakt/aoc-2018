import numpy as np
import networkx as nx


class ZombieUnitError(Exception):
    """Raised if dead unit is attacked."""


class Unit:
    def __init__(self, x, y, race, hp=200, ap=3):
        self.x = x
        self.y = y
        self.race = race
        self._hp = hp
        self.ap = ap

    def __repr__(self):
        return f'({self.x},{self.y}) <{self.race}>'

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __eq__(self, pos):
        return self.pos == pos

    def __hash__(self):
        return id(self)

    @property
    def hp(self):
        return self._hp

    def take_damage(self, dmg):
        if not self.alive:
            raise ZombieUnitError(f'Tried attacking {self.race} with {self.hp} hp')
        self._hp -= dmg

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos):
        self.x, self.y = new_pos

    @property
    def alive(self):
        return self.hp > 0


class Board:
    def __init__(self, map_file='clue.txt', elf_ap=3):
        with open(map_file) as f:
            board = f.read().splitlines()

        self.board = np.array([[pixel for pixel in line] for line in board])

        self.elves = set()
        self.goblins = set()
        self.all_units = set()
        self.rounds = 0

        cols, rows = self.board.shape
        for col in range(cols):
            for row in range(rows):
                pixel = self.board[col,row]
                if pixel == 'E':
                    elf = Unit(row, col, 'elf', ap=elf_ap)
                    self.elves.add(elf)
                    self.all_units.add(elf)
                    self.board[col,row] = '.'
                elif pixel == 'G':
                    goblin = Unit(row, col, 'goblin')
                    self.goblins.add(goblin)
                    self.all_units.add(goblin)
                    self.board[col,row] = '.'

        G = nx.Graph()
        for col in range(cols):
            for row in range(rows):
                if self.board[col,row] != '.':
                    continue
                for x2, y2 in [(-1,0), (0,1), (1,0), (0,-1)]:
                    x, y = row+x2, col+y2
                    if (0,0) <= (y,x) <= self.board.shape and self.board[y,x] == '.':
                        G.add_edge((row,col), (x,y))

        self.graph = G

    def __repr__(self):
        return '({} elves, {} goblins)'.format(len(self.elves), len(self.goblins))

    def __len__(self):
        elves = len(self.elves)
        goblins = len(self.goblins)
        return elves + goblins

    @property
    def combat_end(self):
        if any(unit.alive for unit in self.elves) and any(unit.alive for unit in self.goblins):
            return False
        else:
            return True 

    def next_move(self, cur_unit, target_unit):
        graph = self.graph.copy()

        for unit in self.all_units:
            if unit.pos == cur_unit.pos or unit.pos == target_unit.pos or not unit.alive:
                continue
            graph.remove_node(unit.pos) # remove all other nodes containing units from consideration

        nearest_adjacent = (None,None)
        neighbors = graph.neighbors(cur_unit.pos)

        for node in neighbors:
            try:
                path_length = nx.algorithms.shortest_path_length(graph, node, target_unit.pos)

                if nearest_adjacent == (None, None):
                    nearest_adjacent = (node, path_length)
                elif path_length < nearest_adjacent[1]:
                    nearest_adjacent = (node, path_length)
                elif path_length == nearest_adjacent[1] and node[::-1] < nearest_adjacent[0][::-1]: # if equal, check reading order
                    nearest_adjacent = (node, path_length)
                    
            except nx.NetworkXNoPath:
                pass

        return nearest_adjacent[0]

    def nearest_enemy(self, cur_unit, attack=False):
        nearest = []
        graph = self.graph.copy()

        if cur_unit.race == 'elf':
            enemies = self.goblins
        elif cur_unit.race == 'goblin':
            enemies = self.elves

        for unit in self.all_units:
            if unit is cur_unit or unit in enemies or not unit.alive:
                continue
            graph.remove_node(unit.pos)

        for target_unit in enemies:
            if not target_unit.alive:
                continue
            try:
                path_length = nx.algorithms.shortest_path_length(graph, cur_unit.pos, target_unit.pos)
                nearest.append((target_unit, path_length))
            except nx.NetworkXNoPath:
                pass

        if nearest and not attack:
            return min(nearest, key=lambda enemy: (enemy[1], enemy[0]))
        elif nearest and attack:
            return min(nearest, key=lambda enemy: (enemy[1], enemy[0].hp, enemy[0]))
        else:
            return (None, None)

    def do_round(self, part2=False):
        if self.combat_end:
            return

        units = sorted(self.all_units)
        for unit in units:
            if not unit.alive:
                continue

            # first move
            enemy, path_length = self.nearest_enemy(unit)
            if enemy is not None:
                next_move = self.next_move(unit, enemy)
                if next_move != enemy.pos and next_move is not None:
                    unit.pos = next_move

            # then attack
            enemy, path_length = self.nearest_enemy(unit, True)
            if enemy is not None and path_length == 1:
                enemy.take_damage(unit.ap)

            if part2 and not all(unit.alive for unit in self.elves):
                return

            if self.combat_end and unit == units[-1]:
                self.rounds += 1
                return
            elif self.combat_end:
                return

        self.rounds += 1

    def display(self):
        board = self.board.copy()
        rows, cols = board.shape
        for row in range(rows):
            units = []
            for col in range(cols):
                if (col, row) in [unit.pos for unit in self.elves if unit.alive]:
                    board[row,col] = 'E'
                    elves = list(self.elves)
                    elf = elves[elves.index((col,row))]
                    units.append(elf)
                elif (col, row) in [unit.pos for unit in self.goblins if unit.alive]:
                    board[row,col] = 'G'
                    goblins = list(self.goblins)
                    goblin = goblins[goblins.index((col,row))]
                    units.append(goblin)

                print(board[row,col], end='')
                
            print('  ', end='')
            for unit in sorted(units):
                print(f'{unit.race[0].upper()}({unit.hp})', end=', ')
            print()


board = Board('clue.txt')

# board.display()
# print()
while not board.combat_end:
    board.do_round()
    # board.display()
    # print(test.rounds)
    # print()

print('Part 1:', board.rounds * sum(unit.hp for unit in board.all_units if unit.alive))

# for ap in range(4, 100):        # 19 is the min ap needed
for ap in range(19, 20):        # hardcoded now for reruns
    # print(ap)
    board = Board('clue.txt', ap)

    while not board.combat_end:
        board.do_round()
        if not all(unit.alive for unit in board.elves):
            break
    else:
        break

print('Part 2:', board.rounds * sum(unit.hp for unit in board.all_units if unit.alive))
