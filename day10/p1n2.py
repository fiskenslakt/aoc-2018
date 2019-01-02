import re
from operator import itemgetter


with open('clue.txt') as f:
    points_raw = f.read().splitlines()

point_pattern = r'-?\d+'

points = {}

for point in points_raw:
    x, y, vx, vy = map(int,re.findall(point_pattern, point))
    points[(x, y)] = (vx, vy)

seconds = 1
old_x_max = max(x for (x,y) in points.keys())
older_x_max = old_x_max

for speed in (1_000, 100, 10, 1):
    while True:
        x_points = []
        for (x,_), (vx,_) in points.items():
            x += vx*seconds
            x_points.append(x)

        new_x_max = max(x_points)
        if new_x_max < old_x_max:
            old_x_max = new_x_max
            seconds += speed
        else:
            old_x_max = older_x_max
            if speed == 1:
                seconds -= speed
            else:
                seconds -= speed*2
            break

display = set()

for (x,y), (vx,vy) in points.items():
    x += vx*seconds
    y += vy*seconds
    display.add((x,y))

x_min = min(x for (x,y) in display)
x_max = max(x for (x,y) in display)
y_min = min(y for (x,y) in display)
y_max = max(y for (x,y) in display)    

for row in range(y_min, y_max+1):
    print()
    for col in range(x_min, x_max+1):
        if (col,row) in display:
            print('#', end='')
        else:
            print(' ', end='')

print(f'\n\nPart 2: {seconds}')            

def test(seconds):
    x_points = []
    for (x,_), (vx,_) in points.items():
        x += vx*seconds
        x_points.append(x)

    return max(x_points)
