import re
import numpy as np


with open('clue.txt') as f:
    clay_raw = f.read().splitlines()

# test_data = [
#     'x=1, y=2..7',
#     'y=7, x=1..7',
#     'x=7, y=3..7',
#     'x=4, y=2..4',
#     'x=12, y=1..2',
#     'x=4, y=13..19',
#     'x=15, y=13..19',
#     'y=19, x=4..15',
#     'y=15, x=11..13',
#     'y=16, x=11..13',
#     'y=17, x=11..13',
#     'y=9, x=7..10',
# ]
    
test_data = [
    'x=495, y=2..7',
    'y=7, x=495..501',
    'x=501, y=3..7',
    'x=498, y=2..4',
    'x=506, y=1..2',
    'x=498, y=10..13',
    'x=504, y=10..13',
    'y=13, x=498..504',
]

x_pattern = r'x=(\d+)\.{0,2}(\d+)?'
y_pattern = r'y=(\d+)\.{0,2}(\d+)?'

x_values = []
y_values = []

# for line in clay_raw:
for line in test_data:
    x_values.extend(re.findall(x_pattern, line))
    y_values.extend(re.findall(y_pattern, line))

x_min = min(int(v) for t in x_values for v in t if v) - 1
x_max = max(int(v) for t in x_values for v in t if v) + 1
y_min = min(int(v) for t in y_values for v in t if v)
y_max = max(int(v) for t in y_values for v in t if v)

offset = x_min

ground = np.empty((y_max+1, x_max-offset), dtype=str)
ground[:] = '.'

for x, y in zip(x_values, y_values):
    if not x[1]:
        x = int(x[0]) - offset
        for i in range(int(y[0]), int(y[1])+1):
            ground[i,x] = '#'

    elif not y[1]:
        y = int(y[0])
        for i in range(int(x[0])-offset, int(x[1])-offset+1):
            ground[y,i] = '#'

spring = [500-offset, 0]
ground[spring[1],spring[0]] = '+'

# rows, cols = ground.shape

# for row in range(rows):
#     for col in range(cols):
#         print(ground[row,col], end='')
#     print()

last_stop = []
water = set([tuple(spring)])

while last_stop or spring[1] != y_max-1:
    if ground[spring[1]+1, spring[0]] != '#' and (spring[1]+1, spring[0]) not in water:
        spring[1] += 1
        ground[spring[1],spring[0]] = '|'
        water.add(tuple(spring))
        last_stop.append(spring.copy())
    else:
        # last_stop.append(spring)
        while ground[spring[1],spring[0]-1] != '#':
            spring[0] -= 1
            ground[spring[1],spring[0]] = '~'
            water.add(tuple(spring))
            if ground[spring[1]+1,spring[0]] != '#' and (spring[1]+1,spring[0]) not in water:
                last_stop.append(spring.copy())
                # print(last_stop)
                break
        else:
            # spring = last_stop.pop()
            spring = last_stop[-1]
            while ground[spring[1],spring[0]+1] != '#':
                spring[0] += 1
                ground[spring[1],spring[0]] = '~'
                water.add(tuple(spring))
                if ground[spring[1]+1,spring[0]] != '#' and (spring[1]+1,spring[0]) not in water:
                    last_stop.append(spring.copy())
                    break
            else:
                # spring = last_stop[-1]
                spring = last_stop.pop()
                spring[1] -= 1

print(len(water))
