class Array:

    def __init__(self, capacity=None):
        if capacity:
            self.array= [None] * capacity
        else:
            self.length=0
            self.array= [None] * 100

    def get_length(self):
        return self.length
    
    def add(self, data):
        for i in range(len(self.array)):
            if self.array[i] == None:
                self.array.append(data)
                return True
            i+=1
        return False
    def generate_array(capacity=None):
        if capacity:
            arr= Array(capacity)
        else:
            arr = Array()

        for i in range(len(arr.length)):
            
        
    








