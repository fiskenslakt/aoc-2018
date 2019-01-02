from collections import deque

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def __repr__(self):
        return f'({self.children}, {self.metadata})'

class Tree:
    def __init__(self, license_file):
        self.root = None
        self.insert(license_file)

    def insert(self, license_file):
        children = license_file.popleft()
        entries = license_file.popleft()

        if self.root is None:
            self.root = Node()
            for _ in range(children):
                self.root.children.append(Node())

        self._insert(self.root, license_file)

        for _ in range(entries):
            self.root.metadata.append(license_file.popleft())

    def _insert(self, cur_node, license_file):
        for child in cur_node.children:
            children = license_file.popleft()
            entries = license_file.popleft()

            if children == 0:
                for _ in range(entries):
                    child.metadata.append(license_file.popleft())
            else:
                for _ in range(children):
                    child.children.append(Node())

                self._insert(child, license_file)

                for _ in range(entries):
                    child.metadata.append(license_file.popleft())


def get_node_value(node, value=0):
    if not node.children:
        return sum(node.metadata)

    for index in node.metadata:
        if index <= len(node.children):
            value += get_node_value(node.children[index-1])

    return value
        
                    
with open('clue.txt') as f:
    n = deque(map(int,f.read().split()))

tree = Tree(n)

print(get_node_value(tree.root))
