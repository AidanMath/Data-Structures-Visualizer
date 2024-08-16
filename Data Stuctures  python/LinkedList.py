from Node import Node
import random 
import inspect

#All other methods implemented via 
class LinkedList:

    def __init__(self):
        self.head = None
        self.length = 0

    def add(self, node):
        if self.head is None:
            self.head=node
        elif self.head.next is None:
            self.head.next == node
        else:
            current=self.head.next
            while current.next:
                current=current.next
            current.next=node
        self.length+=1
