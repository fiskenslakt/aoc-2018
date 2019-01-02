from collections import deque


def marble_game(players, last):
    scores = deque([0]*players)
    circle = deque([0])

    for marble in range(1, last+1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[-1] += marble + circle.pop()
            circle.rotate(-1)
            scores.rotate()
        else:
            scores.rotate()
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)


print('Part 1:', marble_game(428, 70825))
print('Part 2:', marble_game(428, 70825*100))
