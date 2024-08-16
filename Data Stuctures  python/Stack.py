import Node
class Stack:
    def __init__(self):
        self.top = None
        self.size = 1

    def is_empty(self):
        return self.top is None


    def __len__(self):
        return self.size

    def __iter__(self):
        current = self.top
        while current:
            yield current
            current = current.next
