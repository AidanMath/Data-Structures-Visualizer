import tkinter as tk
import random
import Node
from Queue import Queue  # Assuming you have a Queue class implemented


class QueueVisualizer:
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

    def draw_queue(self, queue, highlight_node=None):
        self.canvas.delete("all")
        x = self.start_x
        y = self.start_y
        current = queue.front
        while current:
            color = "white"
            if current == highlight_node:
                color = "lightblue"

            self.draw_node(x, y, self.toString(current.data), color)

            if current.next:
                self.draw_arrow(x, y, x + self.spacing, y, "black")

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

    def animate_enqueue(self, app, queue, data):
        new_node = Node.Node(data)  # Create the new node

        def step(current):
            if current is None:
                queue.front = new_node
                queue.rear = new_node
                queue.length+=1
                self.draw_queue(queue, highlight_node=queue.front)
                app.add_log(f"Enqueued {data}. Queue Length: {queue.length}")
                self.show_message(f"Enqueued {data}")
            else:
                self.draw_queue(queue, highlight_node=current)
                self.show_message("Traversing")
                self.canvas.after(self.animation_speed, lambda: step(current.next))

        if queue.front is None:
            step(None)
        else:
            queue.rear.next = new_node
            queue.rear = new_node
            queue.length+=1
            self.draw_queue(queue, highlight_node=queue.rear)
            app.add_log(f"Enqueued {data}. Queue Length: {queue.length}")
            self.show_message(f"Enqueued {data}")

    def animate_dequeue(self, app, queue):
        def step(current):
            if current is None:
                self.draw_queue(queue)
                self.show_message("Queue is empty")
                app.add_log("Queue is empty")
            else:
                self.draw_queue(queue, highlight_node=current)
                self.show_message(f"Dequeuing {current.data}...")
                self.canvas.after(self.animation_speed, lambda: dequeue_node(current))

        def dequeue_node(current):
            if queue.front == current:
                queue.front = current.next
                if queue.front is None:
                    queue.rear = None
            queue.length -= 1
            self.show_message(f"Dequeued {current.data}")
            self.canvas.after(self.animation_speed, lambda: final_step())

        def final_step():
            self.draw_queue(queue)
            self.show_message("Dequeue complete")
            app.add_log(f"Queue Length: {queue.length}")

        step(queue.front)

    def animate_reverse(self, app, queue):
        if not isinstance(queue, Queue):
            self.show_message("Error: Not a Queue object")
            app.add_log("The provided object is not a Queue")
            return

        def reverse_step(nodes, prev_index, current_index):
            if current_index >= len(nodes):
                queue.front = nodes[prev_index] if prev_index >= 0 else None
                queue.rear = nodes[0] if nodes else None
                self.draw_queue(queue)
                self.show_message("Reversed")
                app.add_log("Queue reversed. O(n) operation time.")
                return

            current = nodes[current_index]
            prev = nodes[prev_index] if prev_index >= 0 else None
            next_index = current_index + 1
            next_node = nodes[next_index] if next_index < len(nodes) else None

            # Create a temporary queue to visualize the current state
            temp_queue = Queue()
            for node in nodes:
                # Manually enqueue nodes into temp_queue
                new_node = Node.Node(node.data)
                if temp_queue.rear:
                    temp_queue.rear.next = new_node
                else:
                    temp_queue.front = new_node
                temp_queue.rear = new_node
                temp_queue.length += 1

            # Visualize the current step
            self.canvas.after(self.animation_speed, draw_state(temp_queue, current))
            self.draw_queue(temp_queue, highlight_node=current)
            self.show_message("Reversing")
            
            # Reverse the connection
            if prev_index >= 0:
                nodes[current_index].next = nodes[prev_index]
            else:
                nodes[current_index].next = None

            # Schedule the next step
            self.canvas.after(self.animation_speed, lambda: reverse_step(nodes, current_index, next_index))
        
        def draw_state(temp_queue, current):
             self.draw_queue(temp_queue, highlight_node=current)

        # Convert the queue to a list of nodes for easier manipulation
        nodes = []
        current = queue.front
        while current:
            nodes.append(current)
            current = current.next

        if nodes:
            reverse_step(nodes, -1, 0)
        else:
            self.draw_queue(queue)
            self.show_message("Queue is empty")
            app.add_log(f"Queue Length is {queue.length}")

    def toString(self, data):
        return str(data)
