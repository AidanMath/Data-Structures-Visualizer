import Array
import time
class ArrayVisualizer:
    def __init__(self, canvas):
        self.canvas=canvas
        self.length=20
        self.width=20
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 500  # milliseconds
        self.current_cell = None
    def draw_array(self, array):
        self.canvas.delete("all")
        count=0
        while count<= array.length:
            self.draw_cell(array[count])

    def draw_cell(self, x, y, data, color="white"):
        cell_size = 40  
        half_size = cell_size // 2
        
        self.canvas.create_rectangle(self.start_x - half_size, self.start_y - half_size,
                                    self.start_x + half_size, self.start_y + half_size,
                                    fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(data))
        self.x+=cell_size

import tkinter as tk
import time

class ArrayVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cell_size = 40
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 500  # milliseconds

    def draw_array(self, array, highlight_index=None):
        self.canvas.delete("all")
        for i, value in enumerate(array):
            x = self.start_x + i * self.cell_size
            y = self.start_y
            color = "blue" if i == highlight_index else "white"
            self.draw_cell(x, y, value, color)

    def draw_cell(self, x, y, data, color="white"):
        half_size = self.cell_size // 2
        self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size, fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(data))

    def animate_add(self, array, data):
        count = 0

        def step(count):
            if count < len(array):
                if array[count] is None:
                    array[count] = data
                    self.draw_array(array, highlight_index=count)
                    self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Added {data} at index {count}", anchor="w")
                else:
                    self.draw_array(array, highlight_index=count)
                    self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Checking index {count}", anchor="w")
                    self.canvas.after(self.animation_speed, lambda: step(count + 1))
            else:
                self.canvas.create_text(self.start_x + 200, self.start_y - 50, text="Array is full, resizing...", anchor="w")
                self.canvas.after(self.animation_speed, resize)

        def resize():
            new_size = len(array) * 2
            new_array = [None] * new_size
            for i, value in enumerate(array):
                new_array[i] = value
            array.extend([None] * (new_size - len(array)))
            self.draw_array(array)
            self.canvas.create_text(self.start_x, self.start_y - 50, text=f"Resized array to {new_size}", anchor="w")
            self.canvas.after(self.animation_speed, lambda: step(len(array) // 2))

        step(count)


    def animate_delete(self, array, data, index=None):
        if index is None:
            def step(count):
                if count >= len(array):
                    self.canvas.create_text(self.start_x, self.start_y, text="Data not present within array")
                    return

                self.draw_array(array, highlight_index=count)
                self.canvas.update()  # Force update the canvas
                
                if array[count] == data:
                    # Highlight the node to be deleted
                    self.draw_array(array, highlight_index=count)
                    self.canvas.create_text(self.start_x+150, self.start_y-50, text="Found data. Deleting...")
                    self.canvas.update()  # Force update the canvas
                    
                    # Pause to show the highlighted node before deletion
                    time.sleep(self.animation_speed / 1000)  # Convert milliseconds to seconds
                    
                    del array[count]
                    self.draw_array(array)
                    self.canvas.create_text(self.start_x, self.start_y-50, text="Deleted from array")
                    self.canvas.update()  # Force update the canvas
                else:
                    self.canvas.create_text(self.start_x, self.start_y - 50, text="Checking index", anchor="w")
                    self.canvas.update()  # Force update the canvas
                    time.sleep(self.animation_speed / 1000)  # Convert milliseconds to seconds
                    step(count + 1)

            step(0)
     
        else:
            if 0 <= index < len(array):
                del array[index]
                self.draw_array(array, highlight_index=None)
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Removed from the array O(1) operation")
            else:
                self.canvas.create_text(self.start_x, self.start_y - 50, text="Invalid index")


                    




    
    # def animate_insert(self, data, index)

            
            
            
            


            
                
                



        
