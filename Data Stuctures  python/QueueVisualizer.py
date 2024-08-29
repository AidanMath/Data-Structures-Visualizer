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
        self.canvas.create_text(self.start_x, self.start_y - 50, text=text, font=("Arial", 14), anchor="w", tags="message")

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
                app.add_log(f"Enqueued {data}. Queue Length: {queue.length}, O(1) operation.")
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
            app.add_log(f"Enqueued {data}. Queue Length: {queue.length}, O(1) operation.")
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
            self.canvas.after(self.animation_speed, lambda: final_step(current.data))

        def final_step(data):
            self.draw_queue(queue)
            self.show_message(f"Dequeued: {data}")
            app.add_log(f"Queue Length: {queue.length}, O(1) operation")

        step(queue.front)

    def animate_insert(self, app, queue, data, position):
        new_node = Node.Node(data)
        if position>queue.length:
            app.add_log(f"{position} is larger than the length of the Queue")
            self.show_message(f"{position} is out of range, too large")
        elif position <0:
            app.add_log(f"{position} is less than the length of the Queue")
            self.show_message(f"{position} is out of range, too small")
        else:
            def step(current, index):
                if index == position or current is None:
                    new_node.next = current
                    if index == 0:
                        queue.front = new_node
                        queue.length += 1
                        self.draw_queue(queue, highlight_node=new_node)
                        app.add_log(f"Inserted {data} at Index 0. Queue Length: {queue.length}, O(1) operation.")
                        self.show_message(f"Inserted {data} at position {position}")
                        return
                    else:
                        prev.next = new_node
                    if current is None:
                        queue.rear = new_node
                        queue.length += 1
                        self.draw_queue(queue, highlight_node=new_node)
                        app.add_log(f"Inserted {data} at Index {queue.length}. Queue Length: {queue.length}, O(1) operation.")
                        self.show_message(f"Inserted {data} at position {position}")
                        return
                    queue.length += 1
                    self.draw_queue(queue, highlight_node=new_node)
                    app.add_log(f"Inserted {data} at position {position}. Queue Length: {queue.length}, O(n) operation.")
                    self.show_message(f"Inserted {data} at position {position}")
                else:
                    self.draw_queue(queue, highlight_node=current)
                    self.show_message(f"Traversing to Index: {position}")
                    self.canvas.after(self.animation_speed, lambda: step(current.next, index + 1))

            if position == 0:
                step(queue.front, 0)
            else:
                prev = queue.front
                for _ in range(position - 1):
                    if prev.next is None:
                        break
                    prev = prev.next
                step(prev.next, position)

    def animate_sort(self, app, queue):

        def bubble_sort_step(swapped):
            if not swapped:
                self.draw_queue(queue)
                self.show_message("Queue is sorted")
                app.add_log("Queue sorted, O(n^2) operation")
                return

            current = queue.front
            swapped = False
            while current and current.next:
                if current.data > current.next.data:
                    temp = current.data
                    current.data = current.next.data
                    current.next.data = temp
                    swapped = True
                    self.draw_queue(queue, highlight_node=current)
                    self.show_message(f"Swapped {current.data} and {current.next.data}")
                    self.canvas.after(self.animation_speed, lambda: bubble_sort_step(swapped))
                    return
                current = current.next

            self.canvas.after(self.animation_speed, lambda: bubble_sort_step(swapped))

        bubble_sort_step(True)

    def animate_search(self, app, queue, target):
        front=queue.front
        back=queue.rear
        if front.data== target:
            self.draw_queue(queue, front)
            self.show_message(f"{target} Found at the front")
            app.add_log(f"{target} Is front of the queue, O(1) operation")
        elif back.data==target:
            self.draw_queue(queue, back)
            self.show_message(f"{target} Found at the back")
            app.add_log(f"{target} Is the rear of the queue, O(1) operation")
        else:
            def step(current, index):
                if current is None:
                    self.draw_queue(queue)
                    self.show_message(f"{target} not found in the queue")
                    app.add_log(f"{target} not found in the queue")
                elif current.data == target:
                    self.draw_queue(queue, highlight_node=current)
                    self.show_message(f"Found {target} within the queue")
                    app.add_log(f"Found {target} at position {index}, O(n) operation.")
                else:
                    self.draw_queue(queue, highlight_node=current)
                    self.show_message(f"Searching for {target}...")
                    self.canvas.after(self.animation_speed, lambda: step(current.next, index + 1))

            step(queue.front, 0)
        
    def animate_generate(self, app, queue, length):
        def generate_step(count):
            if count < length:
                data = random.randint(0, 100)
                new_node = Node.Node(data)
                
                if queue.front is None:
                    queue.front = new_node
                    queue.rear = new_node
                else:
                    queue.rear.next = new_node
                    queue.rear = new_node
                
                queue.length += 1
                
                self.draw_queue(queue, highlight_node=queue.rear)
                self.show_message(f"Generated {data}")
                app.add_log(f"Generated {data}. Queue Length: {queue.length}")
                self.canvas.after(self.animation_speed, lambda: generate_step(count + 1))
            else:
                self.draw_queue(queue)
                self.show_message(f"Generated queue with {length} elements")
                app.add_log(f"Generated queue with {length} elements, O(n) operation.")

        # Clear the existing queue
        if queue.front:
            queue.front=None
            queue.length=0
            

        generate_step(0)

    
    def toString(self, data):
        return str(data)
