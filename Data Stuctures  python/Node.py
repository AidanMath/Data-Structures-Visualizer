class Node:

    def __init__(self, data):
        self.next=None
        self.data=data

    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next
    
    def set_next(self, next_node):
        self.next = next_node
    
    def set_data(self, data):
        self.data=data

    def toString(self):
        return print(str(self.data))

    
