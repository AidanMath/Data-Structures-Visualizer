import tkinter as tk
from tkinter import ttk
import random
import Node, LinkedList, Array, Stack, Queue, BinaryTree, HashTable
import LinkedListVisualizer, ArrayVisualizer, StackVisualizer

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
            "LinkedList": ["Add", "Delete", "Insert", "Reverse", "Sort", "Generate"],
            "Array": ["Add", "Delete", "Delete(Index)", "Insert", "Reverse", "Sort", "Binary Search", "Generate"],
            "Queue": ["Add", "Delete", "Insert", "Reverse", "Sort", "Search", "Promote", "View"],
            "Stack": ["Push", "Pop", "Insert", "Peek", "Reverse", "Sort", "Search"],
            "HashTable": ["Add", "Delete", "etc...", "View"],
            "BinaryTree": ["Inorder Traversal", "Preorder Traversal", "Other traversal", "etc...", "View"]
        }
        
        
        self.method_menu = ttk.Combobox(self.left_frame, textvariable=self.method, state="readonly", width=15, font=("Arial", 12, "bold"))
        self.method_menu.pack(pady=(0,50), padx=20)

        # Sets the Method and updates it accordinghly

        self.update_methods(self.option.get())

        # Create confirm button
        self.confirm = tk.Button(self.left_frame, text="Confirm", command=self.execute_method, **BUTTON_STYLE)
        self.confirm.pack(pady=10, padx=20)

        # Initialize LinkedList and its visualizer
        self.linked_list = LinkedList.LinkedList()
        self.ll_visualizer = LinkedListVisualizer.LinkedListVisualizer(self.canvas)

        # Initial array is of length 4 with nothing inside 
        self.array = [None, None, None, None]
        self.array_visualizer = ArrayVisualizer.ArrayVisualizer(self.canvas, self.array)

        #Stack Initilization
        self.stack = Stack.Stack()
        self.stack_visualizer = StackVisualizer.StackVisualizer(self.canvas, self.stack)

        if self.option.get() == None:
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

        This method updates the UI elements to allow user input for the selected method, such as 
        adding, deleting, or inserting data. It also updates the confirm button's state.

        """

        TITLE_STYLE = {"font": ("Arial", 20, "bold"), "bg": "#e0e0e0", "fg": "#333333"}
        LABEL_STYLE = {"font": ("Arial", 16, "bold"), "bg": "#e0e0e0", "fg": "#333333"}
        BUTTON_STYLE = {"font": ("Arial", 10, "bold"), "bg": "white", "fg": "black", "activebackground": "#666666",  "activeforeground": "green", "relief": "raised", "bd": 2, "padx": 2, "pady": 5}
        ENTRY_STYLE = {"font": ("Arial", 14, "bold"), "bg": "white", "fg": "#333333", "insertbackground": "#333333"}

        # First, remove existing widgets if they exist
        for widget in ['data_info_label', 'data_info_entry', 'index_label', 'index_entry']:
            if hasattr(self, widget):
                getattr(self, widget).pack_forget()
                
        if self.method.get() == "Delete(Index)":
            label_text = "Enter Index"
        
        if self.method.get() in ["Add", "Insert", "Delete", "Generate", "Delete(Index)", "Binary Search", "Push"]:
            if self.method.get() == "Generate":
                label_text = "Enter length:"
            elif self.method.get() == "Delete(Index)":
                label_text = "Enter Index"
            elif self.method.get() == "Binary Search":
                label_text= "Enter Target"
            else:
                label_text = "Enter Data:"
            if self.method.get() == "Insert":
                self.index_label = tk.Label(self.left_frame, text="Enter Index:", **LABEL_STYLE)
                self.index_label.pack(pady=(10, 5), padx=50)
                self.index_entry = tk.Entry(self.left_frame, width=10, **ENTRY_STYLE)
                self.index_entry.pack(pady=(0, 10), padx=50)

            self.data_info_label = tk.Label(self.left_frame, text=label_text, **LABEL_STYLE)
            self.data_info_label.pack(pady=(10, 5), padx=50)

            self.data_info_entry = tk.Entry(self.left_frame, width=10, **ENTRY_STYLE)
            self.data_info_entry.pack(pady=(0, 10), padx=50)
            if hasattr(self, 'confirm'):
                self.confirm.pack_forget()
                self.confirm = tk.Button(self.left_frame, text="Confirm", command=self.execute_method, **BUTTON_STYLE)
                self.confirm.pack(pady=(10, 20), padx=50)
        elif self.method.get() == 'Reverse' or self.method.get() == 'Sort' or self.method.get() == "Pop" or self.method.get() =="Peek":
            if hasattr(self, 'confirm'):
                self.confirm.pack_forget()
                self.confirm = tk.Button(self.left_frame, text="Confirm", command=self.execute_method, **BUTTON_STYLE)
                self.confirm.pack(pady=(10, 20), padx=20)
        else:
            self.confirm.pack_forget()
            pass

    def execute_method(self):
        """
        Executes the selected method for the chosen data structure.

        This method retrieves the selected data structure and method, and then performs the
        corresponding operation such as add, delete, insert, etc., and visualizes the results.
        """

        selected_structure = self.display_to_key[self.option.get()]
        selected_method = self.method.get()
        #Linked List Methods
        
        def linked_list_add():
            data=self.data_info_entry.get()
            self.ll_visualizer.animate_add(self, self.linked_list, int(data))

        def linked_list_delete():
            data=self.data_info_entry.get()
            if self.linked_list.head:
                self.ll_visualizer.animate_delete(self, self.linked_list, int(data))

        def linked_list_insert():
            data=self.data_info_entry.get()
            index= self.index_entry.get()
            if self.linked_list.length >= int(index):
                self.ll_visualizer.animate_insert(self, self.linked_list, int(index), int(data))
            else:
                self.add_log("Out of Bounds")

        def linked_list_sort():
            self.ll_visualizer.animate_sort(self, self.linked_list)
        
        # def linked_list_delete_index():
        #     index = self.data_info_entry.get()
        #     self.ll_visualizer.animate_delete(self, self.linked_list, int(index))

       
        def linked_list_reverse():
            self.ll_visualizer.animate_reverse(self, self.linked_list)
            
        def linked_list_generate():
            length=self.data_info_entry.get()
            self.ll_visualizer.animate_generate_random_list(self, self.linked_list, int(length))

    
        #Array Methods 

        def array_add():
            data=self.data_info_entry.get()
            self.array_visualizer.animate_add(self, self.array, int(data))

        def array_delete():
            if self.method.get() == "Delete(Index)":
                self.array_visualizer.animate_delete(self, self.array, index=int(self.data_info_entry.get()), data=0)
            else:
                self.array_visualizer.animate_delete(self, self.array, data=int(self.data_info_entry.get()))
        
        def array_insert():
            data = self.data_info_entry.get()
            index= self.index_entry.get()
            self.array_visualizer.animate_insert(self, self.array, int(data), int(index))
        
        def array_reverse():
            self.array_visualizer.animate_reverse(self, self.array)
            
        def array_sort():
            self.array_visualizer.animate_sort(self, self.array)

        def array_binary_search():
            target = self.data_info_entry.get()
            self.array_visualizer.animate_binary_search(self, self.array, int(target))
        
        def array_generate():
            length=self.data_info_entry.get()
            self.array_visualizer.animate_generate(self, self.array, int(length))
        
        
        #Stack Methods

        def stack_push():
            data=self.data_info_entry.get()
            self.stack_visualizer.animate_push(self, int(data))

        def stack_pop():
            self.stack_visualizer.animate_pop(self)

        def stack_peek():
            self.stack_visualizer.animate_peek(self)

        def stack_reverse():
            self.stack_visualizer.animate_reverse(self)
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
            #"LinkedList": ["Add", "Delete", "Insert", "Reverse", "Sort", "Generate"],
            #Array": ["Add", "Delete", "Delete(Index)", "Insert", "Reverse", "Sort", "Binary Search", "Generate"],
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
                "Reverse": stack_reverse
            }

        }

        # Execute the action if it exists
        if selected_structure in actions and selected_method in actions[selected_structure]:
            actions[selected_structure][selected_method]()
        else:
            self.canvas.create_text(1920/2, 50, text="Invalid Operation")

                
    def update_methods(self, selected_display_option):

        """
        Updates the available methods based on the selected data structure.

        Parameters:
        selected_display_option (str): The name of the selected data structure.
        
        Updates the method menu with the available methods for the selected data structure
        and refreshes the UI elements accordingly.

        """

        selected_key = self.display_to_key[selected_display_option]
        methods = self.methods.get(selected_key, [])

        self.method_menu['values'] = methods

        if methods:
            self.method.set(methods[0])
        else:
            self.method.set("No methods available")

        # Call display_node_info whenever the method changes
        self.display_node_info()

        self.method.trace('w', lambda *args: self.display_node_info())

if __name__ == "__main__":
    root = tk.Tk()
    app = DataStructureVisualizer(root)
    root.mainloop()
