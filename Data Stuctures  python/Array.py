class Array:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * self.capacity
        

    def __len__(self):
        return self.size


    def __iter__(self):
        for i in range(self.size):
            yield self.data[i]
