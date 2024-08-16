import array
import time
import main
import tkinter as tk
import random

class ArrayVisualizer:
    def __init__(self, canvas, array):
        self.canvas = canvas
        self.cell_size = 40
        self.start_x = 50
        self.start_y = 100
        self.animation_speed = 500  # milliseconds
        self.array=array

    def draw_array(self, array, highlight_index=None, highlight_index2=None):
        self.canvas.delete("all")
        for i, value in enumerate(array):
            x = self.start_x + i * self.cell_size
            y = self.start_y
            color = "lightblue" if i == highlight_index or i== highlight_index2 else "white"
            self.draw_cell(x, y, value, color)
        

    def draw_cell(self, x, y, data, color="white"):
        half_size = self.cell_size // 2
        self.canvas.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size, fill=color, outline="black")
        self.canvas.create_text(x, y, text=str(data))

    def clear_message(self):
        self.canvas.delete("message")

    def show_message(self, text):
        self.clear_message()
        self.canvas.create_text(self.start_x, self.start_y - 50, text=text, anchor="w", tags="message")

    def animate_add(self, app, array, data):
        count = 0

        def step(count):
            if count < len(self.array):  # Assuming self.array is the array you're working with
                if self.array[count] is None:
                    self.array[count] = data
                    self.draw_array(self.array, highlight_index=count)
                    app.add_log(f"Added {data} at index {count}. O(n) operation time. Array length: {len(self.array)}")
                    self.show_message("Added Data")
                else:
                    self.draw_array(self.array, highlight_index=count)
                    self.show_message(f"Checking index {count}")
                    self.canvas.after(self.animation_speed, lambda: step(count + 1))
            else:
                self.show_message("Resizing...")
                app.add_log("Array is full, resizing...")
                resize()

        def resize():
            self.show_message("Resizing...")
            new_size = len(self.array) * 2
            new_array = [None] * new_size
            for i, value in enumerate(self.array):
                new_array[i] = value
            self.array = new_array  # Update the array reference in the class or app state
            self.draw_array(self.array)
            
            self.canvas.after(self.animation_speed, lambda: step(len(self.array) // 2))

        step(count)




    def animate_delete(self, app, array, data, index=None):
        if index is None:
            def step(count):
                if count >= len(self.array):
                    app.add_log(f"Looped through whole array and data was not present")
                    return

                self.draw_array(self.array, highlight_index=count)
                self.canvas.update()  # Force update the canvas
                
                if self.array[count] == data:
                    # Highlight the node to be deleted
                    self.draw_array(self.array, highlight_index=count)
                    app.add_log(f"Found Data at index: {count}, deleting now. O(n) operation. Array.length {len(array)-1}")
                
                    self.canvas.update()  # Force update the canvas 
                    
                    # Pause to show the highlighted node before deletion
                    time.sleep(self.animation_speed / 1000)  # Convert milliseconds to seconds
                    
                    del self.array[count]
                    self.draw_array(self.array)
                    self.canvas.update()  # Force update the canvas
                else:
                    self.show_message("Checking index")
                    self.canvas.update()  # Force update the canvas
                    time.sleep(self.animation_speed / 1000)  # Convert milliseconds to seconds
                    step(count + 1)

            step(0)
     
        else:
            index= int(index)
            if 0 <= index < len(self.array):
                self.draw_array(self.array, highlight_index=index)
                self.canvas.update()
                app.add_log(f"Found Data at {index}, Deleting O(1) operation")
                time.sleep(self.animation_speed / 1000) 
                del array[index]
                self.draw_array(self.array, highlight_index=None)
                self.canvas.update()
            else:
                app.add_log(f"Invalid Index, please try Again")


    
    
    def animate_insert(self, app, array, data, index):
        
        index = int(index)
        if index > len(self.array) or index < 0:
            app.add_log("Index out of bounds, please try again")
            self.show_message("Index out of bounds")
        else:
            # Create a new array with an extra slot for the new element
            final_array = [None] * (len(self.array) + 1)
            
            def step(i, state):
                if state == "copy":
                    if i < index:
                        final_array[i] = self.array[i]
                        self.draw_array(final_array, highlight_index=i)
                        app.add_log(f"Copied element {self.array[i]} to new array position {i}")
                        self.canvas.after(self.animation_speed, lambda: step(i + 1, "copy"))
                    else:
                        self.canvas.after(self.animation_speed, lambda: step(index, "insert"))

                elif state == "insert":
                    final_array[index] = data
                    self.draw_array(final_array, highlight_index=index)
                    self.show_message(f"Inserted {data} at index {index}.")
                    app.add_log(f"Inserted element {data} at index {index}")
                    self.canvas.after(self.animation_speed, lambda: step(index, "shift"))

                elif state == "shift":
                    if i < len(self.array):
                        final_array[i + 1] = self.array[i]
                        self.draw_array(final_array, highlight_index=i + 1)
                        app.add_log(f"Shifted element {self.array[i]} to new array position {i + 1}")
                        self.canvas.after(self.animation_speed, lambda: step(i + 1, "shift"))
                    else:
                        self.show_message("Insertion complete")
                        app.add_log(f"Array insertion complete. O(n) operation time. Array.length: {len(final_array)}")
                        self.array[:] = final_array[:]  # Reassign the original array to the new one
            
            # Start the animation by copying elements until the index
            step(0, "copy")

    def animate_generate(self, app, array, length):
        count = 0
        length=int(length)
        final = [None] * (length  )
        def step(count):
           
            if count == length:
                self.array[:] = final[:]  
                self.draw_array(self.array, highlight_index=None)  
                app.add_log(f"Generated Array of Length: {length}. O(n) operation time.")
                self.show_message("Generated Array")
            else:
                add = random.randint(0, 100)
                final[count] = add
                self.draw_array(final, highlight_index=count) 
                self.show_message(f"Generated Data: {add}.")
                app.add_log(f"Generated Data: {add}. At Index: {count}.")
                self.canvas.after(self.animation_speed, lambda: step(count + 1))

        step(0)

    def animate_reverse(self, app, array):
        left=0
        right= len(self.array)-1
        if right==-1:
            self.show_message("Array too small")
            app.add_log("Array unable to reverse due to length")
            return
        if self.array == {None, None, None, None}:
            self.show_message("Array too small")
            app.add_log("Array Empty")

        def step(left, right):
                if left>=right:
                    self.draw_array(self.array, highlight_index=left, highlight_index2=right)
                    app.add_log("Array succesfully reversed, O(n) operation.")
                    self.show_message("Array Reversed")
                else:
                    self.draw_array(self.array, highlight_index=left, highlight_index2=right)
                    self.array[left], self.array[right] = self.array[right], self.array[left]
                    app.add_log(f"Swapped Left Index: {left} with Right Index; {right}")
                    self.show_message("Reversing...")
                    self.canvas.after(self.animation_speed, lambda: step(left + 1, right - 1))
        step(left, right)

    def animate_binary_search(self, app, array, target):
        target = int(target)

        def step(left, right):
            if left > right:
                app.add_log(f"Target: {target} is not found within the array.")
                self.show_message("Target not found.")
                return

            middle = (left + right) // 2
            self.draw_array(self.array, highlight_index=middle)

            if int(self.array[middle]) == target:
                app.add_log(f"Target: {target} was found at Index: {middle}, O(logn) operation.")
                self.show_message("Found target within array")
            elif int(self.array[middle]) > target:
                app.add_log(f"Target: {target} is currently less than Middle index: {middle}.")
                self.show_message("Searching for target...")
                self.draw_array(self.array, highlight_index=middle)
                self.canvas.after(self.animation_speed, lambda: step(left, middle - 1))
            else:
                app.add_log(f"Target: {target} is currently larger than the Middle index: {middle}.")
                self.show_message("Searching for target...")
                self.draw_array(self.array, highlight_index=middle)
                self.canvas.after(self.animation_speed, lambda: step(middle + 1, right))

        step(0, len(self.array) - 1)

    def animate_sort(self, app, array):
        n = len(self.array)

        def step(i, j):
            if i >= n - 1:
                app.add_log("Array successfully sorted, O(n^2) operation.")
                self.show_message("Array sorted")
                return

            if j >= n - i - 1:
                # Move to the next pass
                self.canvas.after(self.animation_speed, lambda: step(i + 1, 0))
            else:
                self.draw_array(self.array, highlight_index=j, highlight_index2=j+1)
                
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    app.add_log(f"Swapped elements at indices {j} and {j+1}.")
                    self.show_message(f"Swapped elements at indices {j} and {j+1}")
                else:
                    app.add_log(f"No swap needed for indices {j} and {j+1}: {self.array[j]} and {self.array[j+1]}")
                    self.show_message(f"Compared elements at indices {j} and {j+1}")

                self.canvas.after(self.animation_speed, lambda: step(i, j + 1))

        step(0, 0)



                

    






            




        



            
            
            
            


            
                
                



        
