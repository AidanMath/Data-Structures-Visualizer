import tkinter as tk
from tkinter import ttk
import random
import Node, LinkedList, Array, Stack, Queue, BinaryTree, HashTable
import LinkedListVisualizer, ArrayVisualizer, StackVisualizer, BinaryTreeVisualizer, QueueVisualizer, HashingTableVisualizer

import ast

class DataStructureVisualizer:
    def __init__(self, master):
        """
    
        master (tk.Tk): The root Tkinter window.

        Sets up the main window, frames, labels, comboboxes, and buttons for the intialization fo the GUI

        """

        # Initializing all the styles that we will be using for widgets and such
        style = ttk.Style()
        style.theme_create("custom", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": "#4a4a4a",
                    "fieldbackground": "white",
                    "background": "white",
                    "foreground": "#333333",
                    "font": ('Helvetica', 20)
                }
            }
        })

        style.theme_use("custom")
        TITLE_STYLE = {"font": ("Arial", 20, "bold"), "bg": "#e0e0e0", "fg": "#333333"}
        LABEL_STYLE = {"font": ("Arial", 16, "bold"), "bg": "#e0e0e0", "fg": "#333333"}
        BUTTON_STYLE = {"font": ("Arial", 10, "bold"), "bg": "white", "fg": "black", "activebackground": "#666666",  "activeforeground": "green", "relief": "raised", "bd": 2, "padx": 2, "pady": 5}
        ENTRY_STYLE = {"font": ("Arial", 14, "bold"), "bg": "white", "fg": "#333333", "insertbackground": "#333333", "relief": "solid"}

    
        self.master = master
        master.title("Data Structure Visualizer")
        master.geometry("1920x1080")

        # Main master window
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both")

        # Left side frame where all info is entered
        self.left_frame = tk.Frame(self.main_frame, width=384, bg="#e0e0e0", padx=15, pady=15)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False) 

        # Title for the left side frame
        control_title = tk.Label(self.left_frame, text="Control Panel", font=("Arial", 20, "bold"), bg="#e0e0e0", fg="#333333")
        control_title.pack(pady=(0, 15))

        # Divider that splits left frame from canvas/rest of the master
        self.divider = tk.Frame(self.main_frame, width=1, bg="#c0c0c0")
        self.divider.pack(side="left", fill="y")

        # This is here the canvas resides and also animation
        self.right_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.right_frame.pack(side="left", fill="both", expand=True)

        # Title for the canvas/animation window
        vis_title = tk.Label(self.right_frame, text="Visualization", font=("Arial", 16, "bold"), bg="#f0f0f0")
        vis_title.pack(pady=(15, 5), side="top")

        #Canvas where we draw on
        self.canvas = tk.Canvas(self.right_frame, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=(5, 20))
        self.canvas.config(bd=1, relief="solid")

        # This is where info can be logged so user can easily follow/access
        info_log = tk.Frame(self.canvas, bg="#f0f0f0", height=200, width=450)
        info_log.pack_propagate(False)
        info_log.pack(side="bottom", padx=20, pady=1)

        # Label for the log
        info_log_label = tk.Label(info_log, text="Current Log", bg="#4a4a4a", fg="white", font=("Arial", 12, "bold"))
        info_log_label.pack(side="top", fill="x")
      

        # Frame where logging happeens
        text_frame = tk.Frame(info_log, bg="#f0f0f0")
        text_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Text widget it logs to
        self.text_widget = tk.Text(text_frame, wrap="word", height=8, width=50, bg="white", fg="#333333", font=("Arial", 10))
        self.text_widget.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.text_widget.config(bd=1, relief="solid")

    

        # Data structure selection
        self.data_structure_label = tk.Label(self.left_frame, text="Select Data Structure:", **LABEL_STYLE)
        self.data_structure_label.pack(pady=(20, 10), padx=20)

        self.display_to_key = {
            "Array": "Array",
            "Binary Tree": "BinaryTree",
            "Linked List": "LinkedList",
            "Stack": "Stack",
            "Queue": "Queue",
            "Hashing Table": "HashTable"
        }

        # The dropdown options fort all the different Data Structures
        self.options = ["Array", "Binary Tree", "Linked List", "Stack", "Queue", "Hashing Table"]

        self.option = tk.StringVar()
        self.option.set("Linked List")
        # Recognizes any changes to the drop box, calls the update method when changes occur
        self.option.trace('w', lambda *args: self.update_methods(self.option.get()))

        # Dropdown for all the Data Strcutures
        self.dropdown = ttk.Combobox(self.left_frame, textvariable=self.option, values=self.options, state="readonly", width=15, font=("Arial", 12, "bold"))
        self.dropdown.pack(pady=(0, 50), padx=20)

        # Method selection
        self.method_label = tk.Label(self.left_frame, text="Select Method:", **LABEL_STYLE)
        self.method_label.pack(pady=(10, 10), padx=20)

        self.method = tk.StringVar()

        # All Methods associated with their respective data structures

        self.methods = {
            "LinkedList": ["Add", "Delete", "Insert", "Reverse", "Sort", "Generate", "Clear"],
            "Array": ["Add", "Delete", "Delete(Index)", "Insert", "Reverse", "Sort", "Binary Search", "Generate", "Clear"],
            "Queue": ["Enqueue", "Dequeue", "Insert", "Sort", "Search", "Generate", "Clear"],
            "HashTable": ["Add", "Delete", "Search","Generate", "Clear"],
            "BinaryTree": ["Add", "Delete", "Inorder Traversal", "Preorder Traversal", "Postorder Traversal", "Generate", "Clear"]
        }
        
        
        self.method_menu = ttk.Combobox(self.left_frame, textvariable=self.method, state="readonly", width=15, font=("Arial", 12, "bold"))
        self.method_menu.pack(pady=(0,50), padx=20)

       

        

      
        # Initialize LinkedList and its visualizer
        self.linked_list = LinkedList.LinkedList()
        self.ll_visualizer = LinkedListVisualizer.LinkedListVisualizer(self.canvas)

        # Initial array is of length 4 with nothing inside 
        self.array = [None, None, None, None]
        self.array_visualizer = ArrayVisualizer.ArrayVisualizer(self.canvas, self.array)

        #Stack Initilization
        self.stack = Stack.Stack()
        self.stack_visualizer = StackVisualizer.StackVisualizer(self.canvas, self.stack)

        self.binary_tree= BinaryTree.BinaryTree()
        self.bt_visualizer = BinaryTreeVisualizer.BinaryTreeVisualizer(self.canvas, self.binary_tree)

        self.queue = Queue.Queue()
        self.queue_visualizer = QueueVisualizer.QueueVisualizer(self.canvas)

        self.hash_visualizer= HashingTableVisualizer.HashingTableVisualizer(self.canvas, 10)

        self.update_methods(self.option.get())

        if self.option.get() == None:
            self.canvas.delete("all")

    def clear_canvas(self):
        """
        Clears all items from the canvas.
        """
        self.canvas.delete("all")

   
    def add_log(self, message):
        """
        Adds a log message to the text widget.

        Parameters:
        message (str): The message to be added to the log.

        """
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.see(tk.END)

    def display_node_info(self):
        """
        Displays input fields and labels for node information based on the selected method.
        """
        LABEL_STYLE = {"font": ("Arial", 16, "bold"), "bg": "#e0e0e0", "fg": "#333333"}
        ENTRY_STYLE = {"font": ("Arial", 14, "bold"), "bg": "white", "fg": "#333333", "insertbackground": "#333333"}
        BUTTON_STYLE = {"font": ("Arial", 10, "bold"), "bg": "white", "fg": "black", "activebackground": "#666666", "activeforeground": "green", "relief": "raised", "bd": 2, "padx": 2, "pady": 5}

        # Remove existing widgets
        self.clear_input_widgets()

        method = self.method.get()
        option = self.option.get()

        if method in ["Add", "Insert", "Delete", "Generate", "Delete(Index)", "Binary Search", "Push", "Search", "Enqueue"]:
            # Determine label text
            if method == "Generate":
                if self.display_to_key[option] == "BinaryTree":
                    label_text = "Enter Depth <=4:"
                elif self.display_to_key[option] == "HashTable":
                    label_text= "Enter Num of Items"
                else:
                    label_text = "Enter length:"
            elif method == "Delete(Index)":
                label_text = "Enter Index:"
            elif method in ["Binary Search", "Search"]:
                label_text = "Enter Target:"
            else:
                label_text = "Enter Data:"

            # Create and pack data entry widgets
            self.data_info_label = tk.Label(self.left_frame, text=label_text, **LABEL_STYLE)
            self.data_info_label.pack(pady=(10, 5), padx=50)
            self.data_info_entry = tk.Entry(self.left_frame, width=10, **ENTRY_STYLE)
            self.data_info_entry.pack(pady=(0, 10), padx=50)

            # Add index entry for Insert method
            if method == "Insert":
                self.index_label = tk.Label(self.left_frame, text="Enter Index:", **LABEL_STYLE)
                self.index_label.pack(pady=(10, 5), padx=50)
                self.index_entry = tk.Entry(self.left_frame, width=10, **ENTRY_STYLE)
                self.index_entry.pack(pady=(0, 10), padx=50)

        # Create and pack confirm button for methods that need it
        if method in ["Add", "Insert", "Delete", "Generate", "Delete(Index)", "Binary Search", "Push", "Search", 
                    "Reverse", "Sort", "Pop", "Peek", "Inorder Traversal", "Preorder Traversal", "Postorder Traversal", "Enqueue", "Dequeue"]:
            self.confirm = tk.Button(self.left_frame, text="Confirm", command=self.execute_method, **BUTTON_STYLE)
            self.confirm.pack(pady=(10, 20), padx=50)

    def clear_input_widgets(self):
        """
        Removes existing input widgets from the left frame.
        """
        widgets = ['data_info_label', 'data_info_entry', 'index_label', 'index_entry', 'confirm']
        for widget in widgets:
            if hasattr(self, widget):
                getattr(self, widget).destroy()
                delattr(self, widget)

    def execute_method(self):
        """
        Executes the selected method for the chosen data structure.
        This method retrieves the selected data structure and method, and then performs the
        corresponding operation such as add, delete, insert, etc., and visualizes the results.
        """

        selected_structure = self.display_to_key[self.option.get()]
        selected_method = self.method.get()
        
    # Utility function to safely convert input to int
        def safe_int_conversion(value):
            try:
                return int(value)
            except ValueError:
                self.add_log("Please enter valid Data.")
                return None

    # Linked List Methods
        def linked_list_add():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.ll_visualizer.animate_add(self, self.linked_list, data)

        def linked_list_delete():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None and self.linked_list.head:
                self.ll_visualizer.animate_delete(self, self.linked_list, data)

        def linked_list_insert():
            data = safe_int_conversion(self.data_info_entry.get())
            index = safe_int_conversion(self.index_entry.get())
            if data is not None and index is not None:
                if self.linked_list.length >= index:
                    self.ll_visualizer.animate_insert(self, self.linked_list, index, data)
                else:
                    self.add_log("Out of Bounds")

        def linked_list_sort():
            self.ll_visualizer.animate_sort(self, self.linked_list)
            
        def linked_list_reverse():
            self.ll_visualizer.animate_reverse(self, self.linked_list)
                
        def linked_list_generate():
            length = safe_int_conversion(self.data_info_entry.get())
            if length is not None:
                self.ll_visualizer.animate_generate_random_list(self, self.linked_list, length)

        # Array Methods
        def array_add():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.array_visualizer.animate_add(self, self.array, data)

        def array_delete():
            if self.method.get() == "Delete(Index)":
                index = safe_int_conversion(self.data_info_entry.get())
                if index is not None:
                    self.array_visualizer.animate_delete(self, self.array, index=index, data=0)
            else:
                data = safe_int_conversion(self.data_info_entry.get())
                if data is not None:
                    self.array_visualizer.animate_delete(self, self.array, data=data)
            
        def array_insert():
            data = safe_int_conversion(self.data_info_entry.get())
            index = safe_int_conversion(self.index_entry.get())
            if data is not None and index is not None:
                self.array_visualizer.animate_insert(self, self.array, data, index)
            
        def array_reverse():
            self.array_visualizer.animate_reverse(self, self.array)
                
        def array_sort():
            self.array_visualizer.animate_sort(self, self.array)

        def array_binary_search():
            target = safe_int_conversion(self.data_info_entry.get())
            if target is not None:
                self.array_visualizer.animate_binary_search(self, self.array, target)
            
        def array_generate():
            length = safe_int_conversion(self.data_info_entry.get())
            if length is not None:
                self.array_visualizer.animate_generate(self, self.array, length)

        # Stack Methods
        def stack_push():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.stack_visualizer.animate_push(self, data)

        def stack_pop():
            self.stack_visualizer.animate_pop(self)

        def stack_peek():
            self.stack_visualizer.animate_peek(self)

        def stack_reverse():
            self.stack_visualizer.animate_reverse(self)
            
        def stack_generate():
            length = safe_int_conversion(self.data_info_entry.get())
            if length is not None:
                self.stack_visualizer.animate_generate(self, length)

        def stack_sort():
            self.stack_visualizer.animate_stack_sort(self)
            
        def stack_search():
            target = safe_int_conversion(self.data_info_entry.get())
            if target is not None:
                self.stack_visualizer.animate_search(self, target)

        def stack_insert():
            index = safe_int_conversion(self.index_entry.get())
            data = safe_int_conversion(self.data_info_entry.get())
            if index is not None and data is not None:
                self.stack_visualizer.animate_insert(self, data, index)
            
        # Binary Tree Methods
        def binary_tree_add():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.bt_visualizer.animate_add(self, data)
            
        def binary_tree_delete():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.bt_visualizer.animate_delete(self, data)
            
        def binary_tree_generate():
            length = safe_int_conversion(self.data_info_entry.get())
            if length is not None:
                self.bt_visualizer.animate_random_tree(self, length)

        def binary_tree_inorder():
            self.bt_visualizer.animate_in_order(self)
            
        def binary_tree_postorder():
            self.bt_visualizer.animate_post_order(self)
            
        def binary_tree_preorder():
            self.bt_visualizer.animate_pre_order(self)

        #Queue Methods
        def queue_enqueue():
            data = safe_int_conversion(self.data_info_entry.get())
            if data is not None:
                self.queue_visualizer.animate_enqueue(self, self.queue, data)

        def queue_dequeue():
            self.queue_visualizer.animate_dequeue(self, self.queue)
        
        def queue_insert():
            data = safe_int_conversion(self.data_info_entry.get())
            index =safe_int_conversion(self.index_entry.get())
            self.queue_visualizer.animate_insert(self, self.queue, data, index)
        
        def queue_sort():
            self.queue_visualizer.animate_sort(self, self.queue)
        
        def queue_search():
            data = safe_int_conversion(self.data_info_entry.get())
            self.queue_visualizer.animate_search(self, self.queue, data)

        def queue_generate():
            length = safe_int_conversion(self.data_info_entry.get())
            self.queue_visualizer.animate_generate(self, self.queue, length)
        
        # Hshing table functions

        def hash_insert():
            key = safe_int_conversion(self.data_info_entry.get())
            self.hash_visualizer.animate_insert(self, key)

        def hash_search():
            key = safe_int_conversion(self.data_info_entry.get())
            self.hash_visualizer.animate_search(self, key)
        
        def hash_generate():
            length= safe_int_conversion(self.data_info_entry.get())
            self.hash_visualizer.animate_generate(self, length)

        def hash_delete():
            data = safe_int_conversion(self.data_info_entry.get())
            self.hash_visualizer.animate_delete(self, data)

        

        # Map structure and method to these regular functions

        actions = {
            "LinkedList": {
                "Add": linked_list_add,
                "Delete": linked_list_delete,
                #"Delete(Index)": linked_list_delete_index,
                "Insert": linked_list_insert,
                "Reverse": linked_list_reverse,
                "Sort": linked_list_sort,
                "Generate": linked_list_generate
                
            },
            
            "Array": {
                "Add": array_add,
                "Delete": array_delete,
                "Delete(Index)": array_delete,
                "Insert": array_insert,
                "Reverse": array_reverse,
                "Sort": array_sort,
                "Binary Search": array_binary_search,
                "Generate": array_generate
            },

            "Stack": {
                "Push": stack_push,
                "Pop": stack_pop,
                "Peek": stack_peek,
                "Reverse": stack_reverse,
                "Generate": stack_generate,  
                "Sort": stack_sort,
                "Search": stack_search,
                "Insert": stack_insert
            },
            "BinaryTree": {
                "Add": binary_tree_add,
                "Delete": binary_tree_delete,
                "Generate": binary_tree_generate,
                "Inorder Traversal": binary_tree_inorder,
                "Postorder Traversal": binary_tree_postorder,
                "Preorder Traversal": binary_tree_preorder
            },
            "Queue": {
                "Enqueue": queue_enqueue,
                "Dequeue": queue_dequeue,
                "Insert": queue_insert,
                "Sort": queue_sort,
                "Search": queue_search,
                "Generate": queue_generate


            },
            "HashTable": {
                "Add": hash_insert,
                "Search": hash_search,
                "Generate": hash_generate,
                "Delete": hash_delete

            }

        }

        # Execute the action if it exists
        if selected_structure in actions and selected_method in actions[selected_structure]:
            # Clear canvas before executing the method
           
            actions[selected_structure][selected_method]()
        else:
            self.canvas.create_text(1920/2, 50, text="Invalid Operation")
                
    def update_methods(self, selected_display_option):
        """
        Updates the available methods based on the selected data structure.
        """
        selected_key = self.display_to_key[selected_display_option]
        methods = self.methods.get(selected_key, [])
        # Clear the canvas before updating methods
        self.clear_canvas()

        self.method_menu['values'] = methods

        if methods:
            self.method.set(methods[0])
        else:
            self.method.set("No methods available")

        # Call display_node_info whenever the method changes
        self.display_node_info()

        

        # Ensure display_node_info is called when the method changes
        self.method.trace('w', lambda *args: self.display_node_info())

if __name__ == "__main__":
    root = tk.Tk()
    app = DataStructureVisualizer(root)
    root.mainloop()
