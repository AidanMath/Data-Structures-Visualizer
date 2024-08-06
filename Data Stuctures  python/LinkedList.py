from Node import Node
import random 
import inspect

# need to add a view Linked List Method, that simply displays current status of a linked list 

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

        #*___EDGE CASES__*
        if self.head is None:
            return False  
        
        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1
            return True
        
        #looping throught to find the node to remove 
        current_node = self.head
        while current_node.next is not None:
            if current_node.next.data == data:#finds the previous to the one that needs to be removed
                current_node.next = current_node.next.next
                self.length -= 1
                return True
            current_node = current_node.next
        
       
        return False  

    def toString(self):

        output = ""
        current_node = self.head
        #loops and finds 
        while current_node is not None:
            output += str(current_node.data) + " --> "
            current_node = current_node.next
        output += "None"
        return output
    
    
    @staticmethod
    def LL_generator(count=None):
        linkedList = LinkedList()

        if count:
            for _ in range(count):
                linkedList.add(random.randint(1, 100))
        else:
            for _ in range(100):
                linkedList.add(random.randint(1, 100))

        return linkedList
    

    def LL_insert(self, index, data):

        if index==1 or index==self.length:
            self.add(data)

        if self.head==None and index>0:
            return Exception("Head is null")
        
        if index>self.length:
            return Exception("out of bounds") 
        
        count=1
        current_node=self.head

        #loops to previous node
        while count < index - 1:
            current_node = current_node.next
            count += 1

        new_node = Node(data)
        new_node.next = current_node.next
        current_node.next = new_node
        self.length += 1

    def LL_reverse(self):
        if self.head==None or self.length==1:
            return Exception("List too Small or non Existant")
        current=self.head
        prev=None
        next=None
        #loops throught the list, 
        #finds next node, set pcurrent node.next to prev
        #iterates
        while current!=None:
            next=current.next
            current.next=prev
            prev=current
            current=next

        #repoints head
        self.head=prev

    def sort(self):
        if self.head is None or self.head.next is None:
            return 
        current=self.head
        while current:
            
            runner=current.next
            

            while runner:
                if(current.data > runner.data):
                    temp = current.data
                    current.data=runner.data
                    runner.data=temp
                runner=runner.next
            current=current.next  


            

                            
# Tests 
# LinkedList1 = LinkedList()

# LinkedList1.add(1)

# LinkedList1.add(18)

# LinkedList1.add(2)
# LinkedList1.add(8)
# Random_List= LinkedList.LL_generator(10)


# print(Random_List.toString())
# Random_List.LL_insert(3, 9)
# Random_List.LL_reverse()


# Random_List.sort()
# print(Random_List.length)
# print(Random_List.toString())




# LinkedList1.delete(4)
# print(LinkedList1.toString())
