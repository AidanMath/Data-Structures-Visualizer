import Node
import random
import tkinter as tk
class LinkedListVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_radius = 20
        self.spacing = 80
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 1000  # milliseconds

    def draw_list(self, linked_list, highlight_node=None, highlight_next=None):
        self.canvas.delete("all")
        x = self.start_x
        y = self.start_y
        current = linked_list.head
        while current:
            color = "lightblue" if current == highlight_node else "white"
            self.draw_node(x, y, current.data, color)
            if current.next:
                color = "red" if current.next == highlight_next else "black"
                self.draw_arrow(x, y, x + self.spacing, y, color)
            x += self.spacing
            current = current.next

    def draw_node(self, x, y, data, color="white"):
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(data))

    def draw_arrow(self, x1, y1, x2, y2, color="black"):
        self.canvas.create_line(x1 + self.node_radius, y1,
                                x2 - self.node_radius, y2,
                                arrow=tk.LAST, fill=color)

    def animate_add(self, linked_list, data):
        def step(node):
            if node is None:
                linked_list.add(data)
                self.draw_list(linked_list, linked_list.head)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Added node", anchor="w")
            elif node.next is None:
                node.next = Node.Node(data)
                self.draw_list(linked_list, node, node.next)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Added node", anchor="w")
            else:
                self.draw_list(linked_list, node)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Traversing", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(node.next))

        step(linked_list.head)

    def animate_delete(self, linked_list, data):
        def step(prev, current):
            if current is None:
                self.draw_list(linked_list)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Node not found", anchor="w")
            elif current.data == data:
                if prev is None:
                    linked_list.head = current.next
                else:
                    prev.next = current.next
                linked_list.length -= 1
                self.draw_list(linked_list, prev, prev.next if prev else None)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Deleted node", anchor="w")
            else:
                self.draw_list(linked_list, current)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Traversing", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(current, current.next))

        step(None, linked_list.head)

    def animate_insert(self, linked_list, index, data):
        def step(current, count):
            if count == index - 1 or current.next is None:
                new_node = Node(data)
                new_node.next = current.next
                current.next = new_node
                linked_list.length += 1
                self.draw_list(linked_list, current, new_node)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Inserted node", anchor="w")
            else:
                self.draw_list(linked_list, current)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Traversing", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(current.next, count + 1))

        if index <= 0 or index > linked_list.length + 1:
            self.draw_list(linked_list)
            self.canvas.create_text(self.start_x, self.start_y - 50, text="Invalid index", anchor="w")
        elif index == 1:
            new_node = Node(data)
            new_node.next = linked_list.head
            linked_list.head = new_node
            linked_list.length += 1
            self.draw_list(linked_list, new_node)
            self.canvas.create_text(self.start_x, self.start_y - 50, text="Inserted at head", anchor="w")
        else:
            step(linked_list.head, 1)

    def animate_reverse(self, linked_list):
        def step(prev, current):
            if current is None:
                linked_list.head = prev
                self.draw_list(linked_list)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Reversed", anchor="w")
            else:
                next_node = current.next
                current.next = prev
                self.draw_list(linked_list, current, prev)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Reversing", anchor="w")
                self.canvas.after(self.animation_speed, lambda: step(current, next_node))

        step(None, linked_list.head)

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