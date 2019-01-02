from math import sqrt

from collections import deque

players = 10
last = 47
marble = 1
scores = deque([0]*players)
circle = deque([0])
offset = 0

for i in range(1, int(sqrt(last))+1):
    if marble > last:
        break
    if i < 2:
        i = 2
    else:
        i = i*i
    for j in range(offset, i, 2):
        print(circle, j, offset)
        if marble > last:
            break
        # print(circle, j, marble)
        if marble % 23 == 0:
            offset = 3 if offset == 1 else 1
            # print('score:', scores[-1], '+', marble, '+', circle[j-offset])
            # scores[-1] += marble + circle[j-offset]
            scores[-1] += marble + circle[j-9]
            scores.rotate()
            circle.remove(circle[j-offset])
        else:
            scores.rotate()
            print((j-offset)%len(circle))
            circle.insert(j-offset, marble)

        marble += 1

print(max(scores))
print(scores)
print('marble:', marble)
