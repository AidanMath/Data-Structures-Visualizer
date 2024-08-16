import Node
import random
import tkinter as tk
import LinkedList, Array, Stack
class LinkedListVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_radius = 20
        self.spacing = 75
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 500  # milliseconds

    def clear_message(self):
        self.canvas.delete("message")

    def show_message(self, text):
        self.clear_message()
        self.canvas.create_text(self.start_x, self.start_y - 50, text=text, anchor="w", tags="message")

    def draw_list(self, linked_list, highlight_node=None, highlight_prev=None, highlight_next=None):
        self.canvas.delete("all")
        x = self.start_x
        y = self.start_y
        current = linked_list.head
        while current:
            color = "white"
            if current == highlight_node:
                color = "lightblue"
            elif current == highlight_prev:
                color = "pink"
            elif current == highlight_next:
                color = "lightgreen"
            
            self.draw_node(x, y, self.toString(current.data), color)
            
            if current.next:
                arrow_color = "red" if (current == highlight_node or current == highlight_prev) else "black"
                self.draw_arrow(x, y, x + self.spacing, y, arrow_color)

            x += self.spacing
            current = current.next

    def draw_node(self, x, y, data, color="white"):
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill=color, outline="black")
        self.canvas.create_text(x, y, text=self.toString(data))

    def draw_arrow(self, x1, y1, x2, y2, color="black"):
        self.canvas.create_line(x1 + self.node_radius, y1,
                                x2 - self.node_radius, y2,
                                arrow=tk.LAST, fill=color)

    def animate_add(self, app, linked_list, data):
        new_node = Node.Node(data)  # Create the new node outside the step function

        def step(node):
            # If the linked list is empty, add the new node as the head
            if node is None:
                linked_list.head = new_node
                linked_list.length += 1
                self.draw_list(linked_list, highlight_node=linked_list.head)
                app.add_log(f"Added Node as linked_list.head: O(1) operation. LinkedList.Length: {linked_list.length}")
                self.show_message(f"Added node as linked_list.head")
            
            # If the linked list only contains the head node (and no next node)
            elif node.next is None:
                linked_list.length += 1
                node.next = new_node
                self.draw_list(linked_list, highlight_node=node, highlight_next=node.next)
                app.add_log(f"Added Node as linked_list.head.next: O(1) operation. LinkedList.Length: {linked_list.length}")
                self.show_message(f"Added node as linked_list.head.next")
            
            # If the current node has a next node, continue traversing
            else:
                self.draw_list(linked_list, highlight_node=node)
                self.show_message("Traversing")
                self.canvas.after(self.animation_speed, lambda: step(node.next))

        # Start the step function with the head of the linked list
        step(linked_list.head)

    def animate_delete(self, app, linked_list, data):
       
        def step(prev, current):
            if current is None:
                self.draw_list(linked_list)
                self.show_message("Node not found")
                app.add_log("Node not present within LinkedList")
                self.canvas.after(self.animation_speed, final_step)
            elif current.data == data:
                self.draw_list(linked_list, highlight_node=current)
                self.show_message(f"Node {data} found, deleting...")
                app.add_log(f"First Node with Data: {data} has been found. O(n) operation time. LinkedList.length: {linked_list.length-1}")
                self.canvas.after(self.animation_speed, lambda: delete_node(prev, current))
            else:
                self.draw_list(linked_list, highlight_node=current)
                self.show_message(f"Traversing (current: {current.data})")
                self.canvas.after(self.animation_speed, lambda: step(current, current.next))

        def delete_node(prev, current):
            if prev is None:
                linked_list.head = current.next
            else:
                prev.next = current.next
            linked_list.length -= 1
            
            self.show_message(f"Deleted node {data}")
            self.canvas.after(self.animation_speed, lambda: redraw_after_delete(prev))

        def redraw_after_delete(prev):
            self.draw_list(linked_list, highlight_node=prev.next if prev else linked_list.head)
            self.canvas.after(self.animation_speed, final_step)

        def final_step():
            self.draw_list(linked_list)
            self.show_message("Deletion complete")
           

        step(None, linked_list.head)

    def animate_reverse(self, app, linked_list):
        def reverse_step(nodes, prev_index, current_index):
            if current_index >= len(nodes):
                linked_list.head = nodes[prev_index]
                self.draw_list(linked_list)
                self.show_message("Reversed")
                app.add_log("List reversed. O(n) operation time. ")
                return

            current = nodes[current_index]
            prev = nodes[prev_index] if prev_index >= 0 else None
            next_index = current_index + 1
            next_node = nodes[next_index] if next_index < len(nodes) else None

            # Create a temporary list to visualize the current state
            temp_list = self.create_temp_list(nodes, prev_index, current_index)
            
            # Visualize current step
            self.draw_list(temp_list, highlight_node=current, highlight_prev=prev, highlight_next=next_node)
            self.show_message("Reversing")
            
            # Reverse the connection
            if prev_index >= 0:
                nodes[current_index].next = nodes[prev_index]
            else:
                nodes[current_index].next = None

            # Schedule the next step
            self.canvas.after(self.animation_speed, lambda: reverse_step(nodes, current_index, next_index))

        # Convert the linked list to a list of nodes for easier manipulation
        nodes = []
        current = linked_list.head
        while current:
            nodes.append(current)
            current = current.next

        if nodes:
            reverse_step(nodes, -1, 0)
        else:
            self.draw_list(linked_list)
            self.show_message("List is empty")
            app.add_log(f"List Length is {linked_list.length}")

    def create_temp_list(self, nodes, prev_index, current_index):
        temp_list = LinkedList.LinkedList()
        
        for i, node in enumerate(nodes):
            # Use original data without conversion
            new_node = Node.Node(node.data)
            
            if i == 0:
                temp_list.head = new_node
            else:
                # Add nodes to temp_list (ignoring prev_index and current_index for now)
                temp_list.add(new_node)
            
            # Set next pointer for the new nodes
            if i > 0:
                prev_node.next = new_node
            
            # Save reference to the current node for setting next pointer
            prev_node = new_node
        
        # Manually set next pointer for the last node
        if prev_node:
            prev_node.next = None

        # Set next pointers based on reversed order
        for i in range(len(nodes)):
            if i < current_index:
                temp_list.head = nodes[current_index] if current_index >= 0 else None
            elif i == current_index:
                nodes[current_index].next = nodes[prev_index] if prev_index >= 0 else None
            else:
                nodes[i].next = nodes[i+1] if i+1 < len(nodes) else None

        return temp_list

            

    def animate_sort(self, app, linked_list):
        def step(current, sorted_end):
            if sorted_end == linked_list.head:
                self.draw_list(linked_list)
                self.show_message("Sorted")
                app.add_log("LinkedList is sorted. O(n^2) operation time.")
            elif current.next == sorted_end:
                self.canvas.after(self.animation_speed, lambda: step(linked_list.head, current))
            else:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                    self.draw_list(linked_list, current, current.next)
                    self.show_message("Swapped")
                    app.add_log(f"Swapped {current.data} with {current.next.data}")
                else:
                    self.draw_list(linked_list, current, current.next)
                    self.show_message("Compared")
                    app.add_log(f"Compared {current.data} with {current.next.data}")
                self.canvas.after(self.animation_speed, lambda: step(current.next, sorted_end))

        if not linked_list.head or not linked_list.head.next:
            self.draw_list(linked_list)
            self.show_message("List too small")
            app.add_log(f"List is currently too small to sort. LinkedList.length: {linked_list.length}")
        else:
            step(linked_list.head, None)

    def animate_generate_random_list(self, app, linked_list, length):
        self.show_message(f"Generating a random list of Length {length}")
        
        def step(count, current):
            if count >= length:
                self.draw_list(linked_list)
                self.show_message("Generation Complete")
            else:
                self.show_message(f"Generating a random list of Length: {length}")
                
                new_node = (Node.Node(random.randint(0, 100)))
                if count == 0:
                    linked_list.head = new_node
                    current = linked_list.head
                    linked_list.length+=1
                else:
                    current.next = new_node
                    current = current.next
                    linked_list.length+=1
                
                
                self.draw_list(linked_list, highlight_node=current)
                self.show_message(f"Generated node {count + 1}")
                app.add_log(f"Generated Node: {count+1}, Data: {current.data}")
                self.canvas.create_text(1920/4+10, 50, text=f"Generating a random list of Length {length}")
                self.canvas.after(self.animation_speed, lambda: step(count + 1, current))

        linked_list.head = None
        linked_list.length = 0
        step(0, None)

    def animate_insert(self, app, linked_list, index, data):
        def step(count, current, prev):
            if index == 0:
                new_node = Node.Node(data)
                new_node.next = linked_list.head
                linked_list.head = new_node
                self.draw_list(linked_list, new_node)
                linked_list.length+=1
                self.show_message(f"Inserted node as the head")
                app.add_log(f"Node added at Index:{index}. O(1) operation: LinkedList.length: {linked_list.length}")
            elif count == index:
                new_node = Node.Node(data)
                new_node.next = current
                prev.next = new_node
                linked_list.length+=1
                self.draw_list(linked_list, new_node, highlight_prev=prev, highlight_next=new_node.next)
                self.show_message(f"Inserted node at index {index}")
                app.add_log(f"Inserted Node at Index: {index}. O(n) operation: LinkedList.length: {linked_list.length}")
            else:
                self.draw_list(linked_list, current, highlight_prev=prev) 
                self.show_message(f"Traversing (current: {count})")
                self.canvas.after(self.animation_speed, lambda: step(count + 1, current.next, current))
            

        if index < 0:
            self.show_message("Index out of bounds")
            app.add_log(f"Index entered is out of bounds: {index}")
        else:
            step(0, linked_list.head, None)

    def toString(self, data):
        return str(data)
            

            


        