class Node:

    def __init__(self, state, depth, parent, cost, action):
        self.state = state
        self.depth = depth
        self.parent = parent
        self.cost = cost
        self.action = action

    def __repr__(self):
        """
        A representation of the class. Useful with functions like print.
        :return: a string
        """
        return f'({self.state})'

    def expand(self, state, cost, action):
        return Node(state=state, parent=self, depth=self.depth + 1, cost=self.cost + cost, action=action)

    def path(self):
        node = self
        path = []
        while node.parent:
            print(node)
            action = node.action
            path.append(action)
            node = node.parent
        return list(reversed(path))
