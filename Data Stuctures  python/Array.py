import random

class Array:

    def __init__(self, capacity=None):
        if capacity:
            self.array = [None] * capacity
            self.length = 0
        else:
            self.length = 0
            self.array = [None] * 100

    def get_length(self):
        return self.length
    
    def add(self, data):
        if self.length >= len(self.array):
            self.double_capacity()
        
        for i in range(self.length):
            if self.array[i] is None:
                self.array[i] = data
                self.length += 1
                
                return True
        
        self.array[self.length] = data
        self.length += 1
   
        return True

    def double_capacity(self):
        new_capacity = len(self.array) * 2  
        
        arr = [None] * new_capacity  
        
        for i in range(self.length):
            arr[i] = self.array[i]  
        
        self.array = arr  

        
        return self.array

    
    @staticmethod
    def generate_array(capacity=None):
        if capacity:
            arr = Array(capacity)
        else:
            arr = Array()
            capacity = 100

        for _ in range(capacity):
            arr.add(random.randint(1, 15))

        return arr
    

    def bubble_sort(self):
        for i in range(self.length):
            for j in range(0, self.length - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.display()


    def rotate_array_right(self, shift_amount):
        arr = Array(self.length)  
        self.display()
        for i in range(self.length):
            new_index = (i + shift_amount) % self.length
            arr.array[new_index] = self.array[i]
            print("rotated right")
            arr.display()
        
        self.array = arr.array 
        
        return self.array

    def rotate_array_left(self, shift_amount):
        self.display()
        arr = Array(self.length)  
        for i in range(self.length):
            new_index = (i - shift_amount) % self.length
            arr.array[new_index] = self.array[i]
            print("rotated left")
            arr.display()
        
        self.array = arr.array 
        
        return self.array
    
    def reverse_Array(self):
        #two pointer method, most efficent 
        left=0
        right=self.length-1
        self.display()
        while left<=right:
            temp = self.array[left]
            self.array[left]=self.array[right]
            self.array[right]=temp
            left+=1
            right-=1
            self.display()
        
        
    
    def display(self):
        return print(str(self.array))


    


# Example usage:


Array2 = Array.generate_array(10)

print(Array2)
#Array2.bubble_sort()
#Array2.rotate_array_right(3)
#Array2.rotate_array_left(3)
Array2.reverse_Array()
print(Array2)

