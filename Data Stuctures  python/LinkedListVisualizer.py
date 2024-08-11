import Node
import random
import tkinter as tk
import LinkedList
class LinkedListVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_radius = 20
        self.spacing = 75
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 500  # milliseconds


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
            self.draw_length(linked_list)
            
            if current.next:
                arrow_color = "red" if (current == highlight_node or current == highlight_prev) else "black"
                self.draw_arrow(x, y, x + self.spacing, y, arrow_color)

            x += self.spacing
            current = current.next
        

    def draw_length(self, linked_list):
        x=1920/2
        y=1000
        self.canvas.create_text(x, y, text=f"{linked_list.length}" )

    def draw_node(self, x, y, data, color="white"):
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill=color, outline="black")
        self.canvas.create_text(x, y, text=self.toString(data))

    def draw_arrow(self, x1, y1, x2, y2, color="black"):
        self.canvas.create_line(x1 + self.node_radius, y1,
                                x2 - self.node_radius, y2,
                                arrow=tk.LAST, fill=color)

    def animate_add(self, linked_list, data):
        

        def step(node):
            if node is None:
                linked_list.add(data)
                self.draw_list(linked_list, linked_list.head)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Added node as linkedlist.head", anchor="w")
                linked_list.length += 1
            elif linked_list.head.next is None:
                linked_list.add(data)
                self.draw_list(linked_list, linked_list.head)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Added node as linkedlist.head.next", anchor="w")
                linked_list.length += 1
            elif node.next is None:
                node.next = Node.Node(data)
                self.draw_list(linked_list, node, node.next)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Added node to end of the list after traversing", anchor="w")
                linked_list.length += 1
            else:
                self.draw_list(linked_list, node)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Traversing", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(node.next))

        step(linked_list.head)

    def animate_delete(self, linked_list, data):
        def clear_message():
            self.canvas.delete("message")

        def show_message(text):
            clear_message()
            self.canvas.create_text(self.start_x, self.start_y - 50, text=text, anchor="w", tags="message")

        def step(prev, current):
            if current is None:
                self.draw_list(linked_list)
                show_message("Node not found")
                self.canvas.after(self.animation_speed, final_step)
            elif current.data == data:
                self.draw_list(linked_list, highlight_node=current)
                show_message(f"Node {data} found, deleting...")
                self.canvas.after(self.animation_speed, lambda: delete_node(prev, current))
            else:
                self.draw_list(linked_list, highlight_node=current)
                show_message(f"Traversing (current: {current.data})")
                self.canvas.after(self.animation_speed, lambda: step(current, current.next))

        def delete_node(prev, current):
            if prev is None:
                linked_list.head = current.next
            else:
                prev.next = current.next
            linked_list.length -= 1
            
            show_message(f"Deleted node {data}")
            self.canvas.after(self.animation_speed, lambda: redraw_after_delete(prev))

        def redraw_after_delete(prev):
            self.draw_list(linked_list, highlight_node=prev.next if prev else linked_list.head)
            self.canvas.after(self.animation_speed, final_step)

        def final_step():
            self.draw_list(linked_list)
            show_message("Deletion complete")

        step(None, linked_list.head)

    def animate_reverse(self, linked_list):
        def reverse_step(nodes, prev_index, current_index):
            if current_index >= len(nodes):
                linked_list.head = nodes[prev_index]
                self.draw_list(linked_list)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Reversed", anchor="w")
                return

            current = nodes[current_index]
            prev = nodes[prev_index] if prev_index >= 0 else None
            next_index = current_index + 1
            next_node = nodes[next_index] if next_index < len(nodes) else None

            # Create a temporary list to visualize the current state
            temp_list = self.create_temp_list(nodes, prev_index, current_index)
            
            # Visualize current step
            self.draw_list(temp_list, highlight_node=current, highlight_prev=prev, highlight_next=next_node)
            self.canvas.create_text(self.start_x, self.start_y - 50, text="Reversing", anchor="w")
            
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
            self.canvas.create_text(self.start_x, self.start_y - 50, text="List is empty", anchor="w")

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

            

    def animate_sort(self, linked_list):

        def step(current, sorted_end):
            if sorted_end == linked_list.head.next:
                self.draw_list(linked_list)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Sorted", anchor="w")
            elif current.next == sorted_end:
                self.canvas.after(self.animation_speed, lambda: step(linked_list.head, current))
            else:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                    self.draw_list(linked_list, current, current.next)
                    self.canvas.create_text(self.start_x, self.start_y - 50, text="Swapped", anchor="w")
                else:
                    self.draw_list(linked_list, current, current.next)
                    self.canvas.create_text(self.start_x, self.start_y - 50, text="Compared", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(current.next, sorted_end))

        if not linked_list.head or not linked_list.head.next:
            self.draw_list(linked_list)
            self.canvas.create_text(self.start_x, self.start_y - 50, text="List too small", anchor="w")
        else:
            step(linked_list.head, None)

    def animate_generate_random_list(self, linked_list, length):
        self.canvas.create_text(1920/2, 50, text=f"Generating a random list of Length {length}")
        
        def step(count, current):
            if count >= int(length):
                self.draw_list(linked_list)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Generation Complete", anchor="w")
            else:
                self.canvas.create_text(1920/2, 50, text=f"Generating a random list of Length: {length}")
                
                new_node = (Node.Node(str(random.randint(0, 100))))
                if count == 0:
                    linked_list.head = new_node
                    current = linked_list.head
                else:
                    current.next = new_node
                    current = current.next
                
                linked_list.length += 1
                self.draw_list(linked_list, highlight_node=current)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Generated node {count + 1}", anchor="w")
                self.canvas.create_text(1920/3, 50, text=f"Generating a random list of Length {length}")
                self.canvas.after(self.animation_speed, lambda: step(count + 1, current))

        linked_list.head = None
        linked_list.length = 0
        step(0, None)

    def animate_insert(self, linkedlist, index, data):
        self.canvas.create_text(1920 / 2, 50, text="Animation Started")

        def step(count, current, prev):
            if index == 0:
                new_node = Node.Node(data)
                new_node.next = linkedlist.head
                linkedlist.head = new_node
                self.draw_list(linkedlist, new_node)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Inserted node at index {index}", anchor="w")
            elif count == index:
                new_node = Node.Node(data)
                new_node.next = current
                prev.next = new_node
                self.draw_list(linkedlist, new_node, highlight_prev=prev)
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Inserted node at index {index}", anchor="w")
            else:
                self.draw_list(linkedlist, current, highlight_prev=prev) 
                
                self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Traversing (current: {count})", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(count + 1, current.next, current))
            linkedlist.length += 1

        if index < 0:
            self.canvas.create_text(self.start_x, self.start_y - 50, text="Index out of bounds", anchor="w")
        else:
            step(0, linkedlist.head, None)

    def toString(self, data):
        return str(data)
            

            


        