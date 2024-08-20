
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.length = 0

    def is_empty(self):
        return self.front is None
