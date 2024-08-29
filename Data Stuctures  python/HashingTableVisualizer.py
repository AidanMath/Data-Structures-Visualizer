import tkinter as tk
import random

class HashingTableVisualizer:
    def __init__(self, canvas, table_size=10):
        self.canvas = canvas
        self.table_size = table_size
        self.cell_width = 60
        self.cell_height = 40
        self.start_x = 50
        self.start_y = 50
        self.animation_speed = 500  # milliseconds
        self.hash_table = [[] for _ in range(table_size)]

    def show_message(self, text):
         self.canvas.create_text(self.start_x, self.start_y - 20,text=text, anchor="w" , font=("Ariel", 14))


    def draw_table(self, highlight_index=None):
        self.canvas.delete("all")
        spacing = 60   
        for i in range(self.table_size):
            x = self.start_x
            y = self.start_y + i * self.cell_height
            # Draw index
            self.canvas.create_text(x-20, y + self.cell_height / 2,
                                    text=str(i), font=("Arial", 12))

            # Draw cell
            fill_color = "lightblue" if i == highlight_index else "white"
            self.canvas.create_rectangle(x, y, x + self.cell_width, y + self.cell_height,
                                        fill=fill_color, outline="black")

            # Draw chain
            current_x = x +30 # Starting position inside the cell

            for j, item in enumerate(self.hash_table[i]):
                text = "None" if item is None else str(item)  # Handle None values
                text_x = current_x
                text_y = y + self.cell_height / 2

                # Draw text
                self.canvas.create_text(text_x, text_y,
                                        text=text, font=("Arial", 12))

                # Draw arrow if not the last item
                if j < len(self.hash_table[i]) - 1:
                    next_x = current_x + spacing
                    self.canvas.create_line(text_x + 20, text_y,
                                            next_x - 20, text_y,
                                            arrow=tk.LAST)

                # Move the starting position for the next item
                current_x += spacing


    def hash_function(self, key):
        return key % self.table_size

    def animate_insert(self, app, key):
        hash_value = self.hash_function(key)
        
        def highlight_step():
            self.draw_table(highlight_index=hash_value)
            self.show_message(text=f"Inserting {key} at index {hash_value}")
            self.canvas.after(self.animation_speed, insert_step)
        
        def insert_step():
            self.hash_table[hash_value].append(key)
            self.draw_table(highlight_index=hash_value)
            self.show_message(text=f"Inserted {key} at index {hash_value}")
            app.add_log(f"Index: {key % self.table_size} = Key: {key} % Table Size: {self.table_sizze}. O(1) operation")

        
        highlight_step()

    def animate_search(self, app, key):
        hash_value = self.hash_function(key)
        
        def search_step(index=0):
            self.draw_table(highlight_index=hash_value)
            if index >= len(self.hash_table[hash_value]):
                self.show_message(text=f"{key} not found")
                return
            
            current_item = self.hash_table[hash_value][index]
            if current_item == key:
                self.show_message(text=f"Found {key} at index {hash_value}, position {index}")
            else:
                self.show_message(text=f"Searching for {key} at index {hash_value}, position {index}")
                self.canvas.after(self.animation_speed, lambda: search_step(index + 1))
        
        search_step()

    def animate_generate(self, app, num_items):
        def generate_step(count):
            if count < num_items:
                key = random.randint(1, 100)
                self.animate_insert(app, key)
                self.canvas.after(self.animation_speed * 2, lambda: generate_step(count + 1))
            else:
                self.draw_table()
                self.show_message(text=f"Generated hash table with {num_items} items")

        self.hash_table = [[] for _ in range(self.table_size)]
        generate_step(0)

    def animate_delete(self, app,  key):
        hash_value = self.hash_function(key)
        
        def search_step(index=0):
            self.draw_table(highlight_index=hash_value)
            if index >= len(self.hash_table[hash_value]):
                self.show_message(text=f"{key} not found for deletion")
                return
            
            current_item = self.hash_table[hash_value][index]
            if current_item == key:
                self.show_message(text=f"Found {key} at index {hash_value}, position {index}. Marking as deleted...")
                
                self.canvas.after(self.animation_speed, lambda: delete_step(index))
            else:
                self.show_message(text=f"Searching for {key} to delete at index {hash_value}, position {index}")
                self.canvas.after(self.animation_speed, lambda: search_step(index + 1))
        
        def delete_step(index):
            self.hash_table[hash_value][index] = None 
            self.draw_table(highlight_index=hash_value)
            self.show_message(text=f"Marked {key} as deleted at index {hash_value}")
            app.add_log(f"Found {key} at index {hash_value}, position {index}. O(1) operation.")
        
        search_step()