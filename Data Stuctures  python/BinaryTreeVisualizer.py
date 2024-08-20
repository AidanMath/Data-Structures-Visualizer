
import math
import tkinter as tk
import BinaryTree
import BTNode
import random 

class BinaryTreeVisualizer:
    def __init__(self, canvas, binary_tree):
        self.canvas = canvas
        self.node_radius = 20
        self.x_spacing = 37  # Reduced from 50
        self.y_spacing = 60  # Reduced from 75
        self.binary_tree = binary_tree
        self.animation_speed = 500  # milliseconds
        
    
        self.start_x = 747
        self.start_y = 50

       
    def draw_tree(self, highlight_node=None):
        self.canvas.delete("tree_elements")  # Clear only tree elements
        if self.binary_tree.root:
            self._draw_node(self.binary_tree.root, self.start_x, self.start_y, 0, highlight_node)


    def _draw_node(self, node, x, y, level, highlight_node):
        color = "lightblue" if node == highlight_node else "white"
        self.draw_node(x, y, self.toString(node.data), color, "tree_elements")

        if node.left:
            child_x = x - self.x_spacing * (2 ** (2 - min(level, 2)))  # Adjusted formula
            child_y = y + self.y_spacing
            self.draw_arrow(x, y, child_x, child_y)
            self._draw_node(node.left, child_x, child_y, level + 1, highlight_node)

        if node.right:
            child_x = x + self.x_spacing * (2 ** (2 - min(level, 2)))  # Adjusted formula
            child_y = y + self.y_spacing
            self.draw_arrow(x, y, child_x, child_y)
            self._draw_node(node.right, child_x, child_y, level + 1, highlight_node)

    def draw_node(self, x, y, data, color="white", tags=None):
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill=color, outline="black", tags=tags)
        self.canvas.create_text(x, y, text=self.toString(data), tags=tags)

    def draw_arrow(self, x1, y1, x2, y2):
        # Calculate the angle of the line
        angle = math.atan2(y2 - y1, x2 - x1)
        
        # Calculate the start and end points of the arrow
        start_x = x1 + self.node_radius * math.cos(angle)
        start_y = y1 + self.node_radius * math.sin(angle)
        end_x = x2 - self.node_radius * math.cos(angle)
        end_y = y2 - self.node_radius * math.sin(angle)
        
        self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, tags="tree_elements")


    
    def clear_message(self):
        self.canvas.delete("message")

    def show_message(self, text):
        self.clear_message()
        self.canvas.create_text(10, 10, text=text, anchor="nw", tags="message")
        
    def animate_add(self, app, data):
        def step(current, parent=None, is_left=None):
            if current is None:
                new_node = BTNode.BTNode(data)
                if parent is None:
                    self.binary_tree.root = new_node
                elif is_left:
                    parent.left = new_node
                else:
                    parent.right = new_node
                app.add_log(f"Added Node with data {data}")
                self.draw_tree(highlight_node=new_node)
                self.show_message(f"Node {data} added successfully")
            elif data < current.data:
                self.draw_tree(highlight_node=current)
                self.show_message(f"Comparing {data} < {current.data}, moving left")
                app.add_log(f"Data {data} is less than current node {current.data}, moving to the Left.")
                self.canvas.after(self.animation_speed, lambda: step(current.left, current, True))
            else:
                self.draw_tree(highlight_node=current)
                self.show_message(f"Comparing {data} >= {current.data}, moving right")
                app.add_log(f"Data {data} is greater than or equal to current node {current.data}, moving to the Right.")
                self.canvas.after(self.animation_speed, lambda: step(current.right, current, False))

        self.canvas.after(0, lambda: step(self.binary_tree.root))

    def animate_delete(self, app, data):
        def step(current, parent):
            if current is None:
                app.add_log(f"{data} not found in the tree.")
                self.show_message(f"{data} not found.")
                return
            
            if current.data == data:
                if current.left is not None and current.right is not None:
                    # Node with two children
                    successor = self.get_min_node(current.right)
                    app.add_log(f"Node {data} has two children, replacing with successor {successor.data}.")
                    current.data = successor.data
                    step(current.right, current)
                elif current.left is not None:
                    # Node with only left child
                    if parent.left == current:
                        parent.left = current.left
                    else:
                        parent.right = current.left
                    app.add_log(f"Node {data} with only left child deleted.")
                elif current.right is not None:
                    # Node with only right child
                    if parent.left == current:
                        parent.left = current.right
                    else:
                        parent.right = current.right
                    app.add_log(f"Node {data} with only right child deleted.")
                else:
                    # Node with no children (leaf node)
                    if parent.left == current:
                        parent.left = None
                    else:
                        parent.right = None
                    app.add_log(f"Leaf node {data} deleted.")
                    
                self.show_message(f"Deleted {data}.")
                self.draw_tree(highlight_node=parent)
            elif data < current.data:
                app.add_log(f"Searching left subtree for {data}...")
                self.show_message("Searching...")
                self.draw_tree(highlight_node=current.left)
                self.canvas.after(self.animation_speed, lambda: step(current.left, current))
            else:
                app.add_log(f"Searching right subtree for {data}...")
                self.show_message("Searching...")
                self.draw_tree(highlight_node=current.right)
                self.canvas.after(self.animation_speed, lambda: step(current.right, current))
        
        if self.binary_tree.root is not None:
            if self.binary_tree.root.data == data:
                # Handle case where root is the node to delete
                pseudo_parent = BTNode.BTNode(None)
                pseudo_parent.left = self.binary_tree.root
                step(self.root, pseudo_parent)
                self.root = pseudo_parent.left
            else:
                step(self.binary_tree.root, None)
        else:
            app.add_log("The tree is empty.")
            self.show_message("The tree is empty.")

    def get_min_node(self, node):
        """Helper method to find the minimum node in the right subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def animate_random_tree(self, app, max_depth):
        
        def add_nodes(current, depth, is_max_depth_side):
            if depth >= max_depth:
                return

            # Vary probability of adding children based on depth and side
            prob = 0.9 if is_max_depth_side else 0.3 + (depth / max_depth) * 0.4

            # Randomly decide to add a left child
            if current.left is None and random.random() < prob:
                current.left = BTNode.BTNode(random.randint(1, 100))
                self.draw_tree(highlight_node=current.left)
                app.add_log(f"Added left child {current.left.data} at depth {depth}")
                self.canvas.after(self.animation_speed, lambda: add_nodes(current.left, depth + 1, is_max_depth_side))

            # Randomly decide to add a right child
            if current.right is None and random.random() < prob:
                current.right = BTNode.BTNode(random.randint(1, 100))
                self.draw_tree(highlight_node=current.right)
                app.add_log(f"Added right child {current.right.data} at depth {depth}")
                self.canvas.after(self.animation_speed, lambda: add_nodes(current.right, depth + 1, is_max_depth_side))

        def create_initial_node():
            self.binary_tree.root = BTNode.BTNode(random.randint(1, 100))
            self.draw_tree(highlight_node=self.binary_tree.root)
            app.add_log(f"Root node {self.binary_tree.root.data} created")
            self.show_message("Generating Random Binary Tree")
            
            # Randomly decide which side will potentially reach max depth
            is_left_max = random.choice([True, False])
            add_nodes(self.binary_tree.root, 1, is_left_max)

            # Generate the other side with varying depth
            add_nodes(self.binary_tree.root, 1, not is_left_max)

        if max_depth < 1:
            app.add_log("Invalid depth. Depth should be at least 1.")
            self.show_message("Invalid depth. Please enter a depth of at least 1.")
        else:
            self.canvas.after(0, create_initial_node)

    def animate_in_order(self, app):
        if self.binary_tree.root is None:
            self.show_message("Empty Binary Tree")
            app.add_log("Add Nodes or generate a Binary Tree in order to use this method.")
            return
        nodes=[]
        def step(current, delay=0):
            if current is None:
                
                return delay

            # Traverse the left subtree first
            delay = step(current.left, delay)

            # Visit the current node
            self.canvas.after(delay, lambda: visit_node(current))
            delay += self.animation_speed  # Increment the delay after visiting

            # Traverse the right subtree
            delay = step(current.right, delay)

            return delay

        def visit_node(node):
            nodes.append(node.data)
            self.draw_tree(highlight_node=node)
            app.add_log(f"Visited node with data {node.data}")
            app.add_log(f"Visited Nodes: {nodes}")
            self.show_message(f"Visited node {node.data}")
        
        app.add_log(f"Visited  Nodes: {nodes}")

        # Start the in-order traversal with an initial delay of 0
        self.canvas.after(0, lambda: step(self.binary_tree.root))
    def animate_post_order(self, app):
        if self.binary_tree.root is None:
            self.show_message("Empty Binary Tree")
            app.add_log("Add Nodes or generate a Binary Tree in order to use this method.")
            return
        nodes=[]
        def step(current, delay=0):
            if current is None:
                return delay

            # Traverse the left subtree first
            delay = step(current.left, delay)

            # Traverse the right subtree
            delay = step(current.right, delay)

            # Visit the current node
            self.canvas.after(delay, lambda: visit_node(current))
            delay += self.animation_speed  # Increment the delay after visiting

            return delay

        def visit_node(node):
            nodes.append(node.data)
            self.draw_tree(highlight_node=node)
            app.add_log(f"Visited node with data {node.data}")
            app.add_log(f"Visited Nodes: {nodes}")
            self.show_message(f"Visited node {node.data}")

        # Start the post-order traversal with an initial delay of 0
        self.canvas.after(0, lambda: step(self.binary_tree.root))

    def animate_pre_order(self, app):
        if self.binary_tree.root is None:
            self.show_message("Empty Binary Tree")
            app.add_log("Add Nodes or generate a Binary Tree in order to use this method.")
            return
        nodes=[]
        def step(current, delay=0):
            if current is None:
                return delay

            self.canvas.after(delay, lambda: visit_node(current))
            delay += self.animation_speed  # Increment the delay after visiting


            delay = step(current.left, delay)

            delay = step(current.right, delay)

            return delay

        def visit_node(node):
            self.draw_tree(highlight_node=node)
            nodes.append(node.data)
            app.add_log(f"Visited node with data {node.data}")
            app.add_log(f"Visited Nodes: {nodes}")
            self.show_message(f"Visited node {node.data}")


        self.canvas.after(0, lambda: step(self.binary_tree.root))
            

    def toString(self, data):
        return str(data)