import numpy as np
from tqdm import tqdm


def get_powerlevel(square):
    serial_no = 4455
    x, y = square
    rack_id = x + 10
    power_level = ((((rack_id * y) + serial_no) * rack_id) // 100 % 10) - 5

    return power_level


grid = np.zeros(shape=(301,301))

for y in range(1,301):
    for x in range(1,301):
        grid[y][x] = get_powerlevel((x,y))

best_submatrix = None
best_powerlevel = 0

grid = grid.cumsum(axis=0).cumsum(axis=1)

for y2 in range(3, 301):
    for x2 in range(3, 301):
        x1, y1 = x2-2, y2-2
        power_level = grid[y2,x2] - grid[y2, x1-1] - grid[y1-1, x2] + grid[y1-1, x1-1]
        if power_level > best_powerlevel:
            best_powerlevel = int(power_level)
            best_submatrix = (x1,y1)

x, y = best_submatrix
print(f'Part 1: {x},{y} | pwrlvl: {best_powerlevel}\n')

for size in tqdm(range(1,301)):
    for y2 in range(size, 301-size+1):
        for x2 in range(size, 301-size+1):
            x1, y1 = x2-size+1, y2-size+1
            power_level = grid[y2,x2] - grid[y2, x1-1] - grid[y1-1, x2] + grid[y1-1, x1-1]
            if power_level > best_powerlevel:
                best_powerlevel = int(power_level)
                best_submatrix = (x1,y1,size)            

x, y, size = best_submatrix
print(f'\nPart 2: {x},{y},{size} | pwrlvl: {best_powerlevel}')
