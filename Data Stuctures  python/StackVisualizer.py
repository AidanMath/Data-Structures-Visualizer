import Stack
import Node
import random
class StackVisualizer:
    def __init__(self, canvas, stack):
        self.canvas = canvas
        self.stack_width = 80
        self.stack_height = 40
        self.animation_speed = 500
        self.stack=stack

    def clear_message(self):
        self.canvas.delete("message")

    def show_message(self, text):
        self.clear_message()
        x_center = self.canvas.winfo_width() // 2  # Center the text horizontally
        self.canvas.create_text(
            x_center, 40,
            text=text,
            anchor="center", 
            tags="message", 
            font=("Arial", 14)
        )
        self.canvas.update_idletasks()  

    def draw_stack(self, highlight_node=None, second_stack=None):
        
        self.canvas.delete("stack_elements")
        x_center = self.canvas.winfo_width() // 2 
        if self.stack.is_empty() and (second_stack is None or second_stack.is_empty()):
            self.show_message("Length of Stack is 0")
            return
        if second_stack:
            temp = Stack.Stack()
            temp2 = Stack.Stack()
            y_position = self.canvas.winfo_height() -240

            while not self.stack.is_empty():
                current = self.stack.top
                self.stack.top = current.next
                current.next = temp.top
                temp.top = current

            while not second_stack.is_empty():
                current = second_stack.top
                second_stack.top = current.next
                current.next = temp2.top
                temp2.top = current
            
            while not temp.is_empty():
                current = temp.top
                temp.top = current.next

                color = "lightblue" if current == highlight_node else "white"
                self.draw_cell(current.data, x_center-100, y_position, color)
                y_position -= self.stack_height
                current.next = self.stack.top
                self.stack.top = current

            y_position = self.canvas.winfo_height() -240
            while not temp2.is_empty():
                current = temp2.top
                temp2.top = current.next

                color = "lightblue" if current == highlight_node else "white"
                self.draw_cell(current.data, x_center + 100, y_position, color)
                y_position -= self.stack_height
                current.next = second_stack.top
                second_stack.top = current
            
        else:
            temp_stack = Stack.Stack()
            y_position = self.canvas.winfo_height() -240  # Start drawing from the top

            # Reverse the stack to draw it from top to bottom
            while not self.stack.is_empty():
                current = self.stack.top
                self.stack.top = current.next
                current.next = temp_stack.top
                temp_stack.top = current

            # Draw the stack from the temporary stack
            while not temp_stack.is_empty():
                current = temp_stack.top
                temp_stack.top = current.next
                color = "lightblue" if current == highlight_node else "white"
                self.draw_cell(current.data, x_center, y_position, color)
                y_position -= self.stack_height

                # Restore the original stack order
                current.next = self.stack.top
                self.stack.top = current

    def draw_cell(self, data, x_center, y_position, color):
         # Center of the canvas for horizontal alignment
        
        self.canvas.create_rectangle(
            x_center - self.stack_width // 2, y_position,
            x_center + self.stack_width // 2, y_position + self.stack_height,
            fill=color,tags="stack_elements"
        )

        self.canvas.create_text(
            x_center, y_position + self.stack_height // 2,  # Center the text in the middle of the rectangle
            text=str(data),
            fill="black",tags="stack_elements"
        )

    def animate_push(self, app,  data):
        new_node = Node.Node(data)

        
        def step():
            self.draw_stack(self.stack)
            self.show_message(f"Pushing...")
            self.canvas.after(self.animation_speed, add_Node)
            self.draw_stack(self.stack)

        def add_Node():
            # Push operation directly on the stack passed
            new_node.next = self.stack.top
            self.stack.top = new_node
            self.draw_stack(highlight_node=self.stack.top)  # Highlight the top of the stack
            app.add_log(f"Pushed {data} onto the stack. Stack size: {len(self.stack)}, O(1) operation.")
            self.show_message("Pushed Data")
            self.stack.size += 1
        step()
        


    def animate_pop(self, app):
        def step():
            self.draw_stack(highlight_node=self.stack.top)
            app.add_log(f"Removing Stack.top: {self.stack.top.data if self.stack.top else 'None'}, O(1) operation.")
            self.show_message("Popping top element")
            self.canvas.after(self.animation_speed, remove)

        def remove():
            if self.stack.is_empty():
                self.show_message("Stack is empty, cannot pop")
                return
            
            current = self.stack.top
            self.stack.top = current.next
            self.show_message(f"Removed:{current.data} from the top of the Stack")

            self.stack.size -= 1
            app.add_log(f"Removed {current.data} from the top of the stack, O(1), length: {self.stack.size}")
            self.draw_stack()

        step()

    def animate_peek(self, app):

        def step():
            self.draw_stack()
            self.show_message("Peeking...")
            self.canvas.after(self.animation_speed, peek)
        def peek():
            self.draw_stack(highlight_node=self.stack.top)
            app.add_log(f"Top of the Stack: {self.stack.top.data}")
            self.show_message(f"Top of the Stack is {self.stack.top.data}")
        step()
    
    def animate_reverse(self, app):
        self.show_message("Starting reverse...")
        temp = Stack.Stack()

        def step():
            nonlocal temp
            if self.stack.is_empty():
                app.add_log("Finished")
                self.show_message("Finished")
                self.stack, temp = temp, self.stack
                self.draw_stack()
                return

            self.draw_stack(highlight_node=self.stack.top, second_stack=temp)
            # Schedule the next step
            self.canvas.after(self.animation_speed, transfer)

        def transfer():
            app.add_log("Reversing...")
            if not self.stack.is_empty():
                current = self.stack.top
                self.stack.top = self.stack.top.next
                current.next = temp.top
                temp.top = current
                temp.size += 1

                # Draw the updated stacks with highlighting
                self.draw_stack(highlight_node=temp.top, second_stack=temp)
                # Schedule the next step
                self.canvas.after(self.animation_speed, step)
            else:
                step()  # Final call to step after the last transfer

        step()  # Start the animation


    def animate_generate(self, app, length):
        
        self.stack.top=None
        def step(count):
            if count == length:
                self.draw_stack(highlight_node=self.stack.top)
                app.add_log(f"Generated Stack of length: {length}")
                self.show_message("Generation complete")
                return
            else:
                current= Node.Node(random.randint(1,100))
                current.next=self.stack.top
                self.stack.top=current
                self.stack.size+=1
                app.add_log(f"Added: {current.data}, O(1) operation")
                self.show_message(f"Generating... ")
                self.draw_stack(highlight_node=self.stack.top)
                self.canvas.after(self.animation_speed, lambda: step(count+1))
        step(0)

    def animate_stack_sort(self, app):
        temp_stack = Stack.Stack()

        def update_message(message):
            self.show_message(message)
            

        def transfer_step():
            if not self.stack.is_empty():
                current = self.stack.top
                self.stack.top = self.stack.top.next
                current.next = None  # Disconnect from original stack
                app.add_log(f"Popped {current.data} from original stack")
                update_message(f"Sorting... Comparing {current.data}")
                self.canvas.after(self.animation_speed, lambda: insert_step(current))
            else:
                # Transfer back to original stack
                self.canvas.after(self.animation_speed, transfer_back_step)

        def insert_step(current):
            if not temp_stack.is_empty() and temp_stack.top.data > current.data:
                popped = temp_stack.top
                temp_stack.top = temp_stack.top.next
                popped.next = self.stack.top
                self.stack.top = popped
                app.add_log(f"Moved {popped.data} back to original stack")
                update_message(f"Comparing {current.data} with {popped.data}")
                self.draw_stack(highlight_node=self.stack.top, second_stack=temp_stack)
                self.canvas.after(self.animation_speed, lambda: insert_step(current))
            else:
                current.next = temp_stack.top
                temp_stack.top = current
                app.add_log(f"Pushed {current.data} to temporary stack")
                update_message(f"Inserted {current.data} into temporary stack")
                self.draw_stack(highlight_node=temp_stack.top, second_stack=temp_stack)
                self.canvas.after(self.animation_speed, transfer_step)

        def transfer_back_step():
            if not temp_stack.is_empty():
                current = temp_stack.top
                temp_stack.top = temp_stack.top.next
                current.next = self.stack.top
                self.stack.top = current
                app.add_log(f"Transferred {current.data} back to original stack")
                update_message(f"Finalizing... Moving {current.data}")
                self.draw_stack(highlight_node=self.stack.top, second_stack=temp_stack)
                self.canvas.after(self.animation_speed, transfer_back_step)
            else:
                app.add_log("Sorting completed")
                update_message("Sorting completed")
                self.draw_stack()

        update_message("Starting sort...")
        self.canvas.after(self.animation_speed, transfer_step)

    def animate_search(self, app, target):
        temp = Stack.Stack()

     

        def step():
            self.show_message("Looking for target")
            if self.stack.is_empty():
                self.show_message("Not in Stack")
                self.canvas.after(self.animation_speed, transfer_back)
            else:
                self.draw_stack(highlight_node=self.stack.top, second_stack=temp)
                self.canvas.after(self.animation_speed, transfer)

        def transfer():
            if self.stack.is_empty():
                self.show_message("Target not found")
                self.canvas.after(self.animation_speed, transfer_back)
            else:
                current = self.stack.top
                self.stack.top = self.stack.top.next
                if current.data == target:
                    app.add_log(f"Target {target} found")
                    self.show_message(f"Target {target} found!")
                    current.next = temp.top
                    temp.top = current
                    self.draw_stack(highlight_node=current, second_stack=temp)
                    self.canvas.after(self.animation_speed, transfer_back)
                else:
                    app.add_log(f"Checking {current.data}")
                    self.show_message(f"Checking {current.data}")
                    current.next = temp.top
                    temp.top = current
                    self.draw_stack(highlight_node=current, second_stack=temp)
                    self.canvas.after(self.animation_speed, transfer)

        def transfer_back():
            if temp.is_empty():
                self.show_message("Search completed")
                self.draw_stack()
            else:
                current = temp.top
                temp.top = temp.top.next
                current.next = self.stack.top
                self.stack.top = current
                app.add_log(f"Transferring {current.data} back to original stack")
                self.show_message(f"Transferring back: {current.data}")
                self.draw_stack(highlight_node=current, second_stack=temp)
                self.canvas.after(self.animation_speed, transfer_back)

        step()

    def animate_insert(self, app, data, index):
        add= Node.Node(data)
        if self.stack.size==0:
            app.add_log("Stack too small")
        elif index>self.stack.size or index<0:
            app.add_log("Index out of range")

        current=self.stack.top

    def animate_insert(self, app, data, index):
        add = Node.Node(data)
        
        if self.stack.size == 0:
            app.add_log("Stack is empty")
            return
        elif index > self.stack.size or index < 0:
            app.add_log("Index out of range")
            return


        count = 0

        def step(count, current):
            # To modify 'current' inside the nested function
            
            if count == index-1:
                add.next = current.next  # Fixing the pointer to the next node
                current.next = add       # Inserting the new node
                app.add_log(f"Added to index: {index}")
                self.show_message("Added")
                self.draw_stack(highlight_node=add)
            else:
                app.add_log(f"Searching... current index: {count}")
                self.show_message(f"Searching...")
                self.draw_stack(highlight_node=current)
                self.canvas.after(self.animation_speed, lambda: step(count + 1, current.next))

        step(0, self.stack.top)  

                




            
