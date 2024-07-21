from Node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def add(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next

            current_node.next = Node(data)
        
        self.length += 1
        return True
    
    def delete(self, data):
        if self.head is None:
            return False  # No List
        
        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1
            print(f"Removed {data} from the head")
            return True
        
        current_node = self.head
        while current_node.next is not None:
            if current_node.next.data == data:
                current_node.next = current_node.next.next
                self.length -= 1
                print(f"Removed {data}")
                return True
            current_node = current_node.next
        
        print(f"Data {data} not found")
        return False  # Data not found

    def toString(self):
        output = ""
        current_node = self.head
        while current_node is not None:
            output += str(current_node.data) + " --> "
            current_node = current_node.next
        output += "None"
        return output

# Example usage
# At the end of your file, add these lines:

print("Starting the program")
LinkedList1 = LinkedList()
print("LinkedList created")
LinkedList1.add(1)
print("Added 1")
LinkedList1.add(2)
print("Added 2")
LinkedList1.add(3)
print("Added 3")
LinkedList1.add(4)
print("Added 4")

print("After adding:", LinkedList1.toString())

LinkedList1.delete(4)
print("After deleting 4:", LinkedList1.toString())

print("Program finished")