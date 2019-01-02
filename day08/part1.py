with open('clue.txt') as f:
    n = map(int,f.read().split())

node_stack = []
entry_stack = []
metadata_sum = 0

for i in n:
    if not node_stack and metadata_sum == 0:
        node_stack.append(i)

    elif len(entry_stack) < len(node_stack):
        entry_stack.append(i)

    elif node_stack[-1] > 0:
        node_stack.append(i)
    else:
        if entry_stack[-1] > 0:
            metadata_sum += i
            entry_stack[-1] -= 1
        if entry_stack[-1] == 0:
            entry_stack.pop()
            node_stack.pop()
            if node_stack:
                node_stack[-1] -= 1

print(metadata_sum)
