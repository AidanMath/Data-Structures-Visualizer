import tkinter as tk
from tkinter import ttk
import random
import LinkedListVisualizer, LinkedList, Array, HashTable, Queue, Stack, BinaryTree
import ast

class DataStructureVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Data Structure Visualizer")
        master.geometry("1920x1080")

        self.color_schemes = {
            "light": {
                "bg": "#F0F0F0",
                "fg": "#000000",
                "button": "#FFFFFF",
                "accent": "#007BFF"
            },
            "dark": {
                "bg": "#2C2C2C",
                "fg": "#FFFFFF",
                "button": "#444444",
                "accent": "#1E90FF"
            }
        }

        self.current_mode = "light"

        # Create main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(expand=True, fill="both")

        # Create left frame for controls (1/5 of the window)
        self.left_frame = tk.Frame(self.main_frame, width=384)  # 1920 / 5 = 384
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)  # Prevent the frame from shrinking

        # Create divider
        self.divider = tk.Frame(self.main_frame, width=2, bd=0, relief="raised")
        self.divider.pack(side="left", fill="y")

        # Create right frame for visualization (4/5 of the window)
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Create canvas for visualization
        self.canvas = tk.Canvas(self.right_frame, bg="white")
        self.canvas.pack(expand=True, fill="both", padx=20, pady=20)

        # Create and pack the theme toggler
        self.background_toggler = tk.Button(self.left_frame, text="Toggle Theme", command=self.theme_switch)
        self.background_toggler.pack(pady=(20, 40), padx=20)

        # Data structure selection
        self.data_structure_label = tk.Label(self.left_frame, text="Select Data Structure:", font=("Times New Roman", 18, "bold"))
        self.data_structure_label.pack(pady=(0, 10), padx=20)

        self.display_to_key = {
            "Arrays": "Array",
            "Binary Tree": "BinaryTree",
            "Linked List": "LinkedList",
            "Stack": "Stack",
            "Queue": "Queue",
            "Hashing Table": "HashTable"
        }
        
        self.options = list(self.display_to_key.keys())
        
        self.option = tk.StringVar()
        self.option.set("Linked List")
        self.option.trace('w', lambda *args: self.update_methods(self.option.get()))

        self.dropdown = ttk.Combobox(self.left_frame, textvariable=self.option, values=self.options, state="readonly", width=25)
        self.dropdown.pack(pady=(0, 40), padx=20)

        # Method selection
        self.method_label = tk.Label(self.left_frame, text="Select Method:", font=("Times New Roman", 18, "bold"))
        self.method_label.pack(pady=(0, 10), padx=20)

        self.method = tk.StringVar()
        self.methods = {
            "LinkedList": ["Add", "Delete", "Insert", "Reverse", "Sort", "View", "Generate"],
            "Array": ["Add", "Delete", "Insert", "Reverse", "Sort", "Binary Search", "View"],
            "Queue": ["Add","Delete", "Insert", "Reverse", "Sort", "Search", "Promote", "View"],
            "Stack": ["Enqueue", "Dequeue", "Insert", "Peek","Reverse", "Sort", "View"],
            "HashTable": ["Add", "Delete", "etc...", "View"],
            "BinaryTree": ["Inorder Traversal", "Preorder Traversal", "Other traversal", "etc...", "View"]
        }

        self.method_menu = ttk.Combobox(self.left_frame, textvariable=self.method, state="readonly", width=25)
        self.method_menu.pack(pady=(0, 40), padx=20)

        self.update_methods(self.option.get())




        # Create confirm button
        self.confirm = tk.Button(self.left_frame, text="Confirm", font=("Arial", 12), command=self.execute_method)
        self.confirm.pack(pady=(0, 20), padx=20)

        if self.option.get() =="Linked List":
            

        # Initialize LinkedList and its visualizer
            self.linked_list = LinkedList.LinkedList()
            self.ll_visualizer = LinkedListVisualizer.LinkedListVisualizer(self.canvas)

        self.apply_theme()

    def remove_button(self, button):
        self.canvas.delete(button)

    def display_node_info(self):
    # First, remove existing widgets if they exist
        for widget in ['node_info_label', 'node_info_entry', 'index_label', 'index_entry']:
            if hasattr(self, widget):
                getattr(self, widget).pack_forget()
        
        if self.method.get() in ["Add", "Insert", "Delete", "Generate"]:
            if self.method.get() == "Generate":
                label_text = "Enter length:"
            else:
                label_text = "Enter node info:"
            if self.method.get() == "Insert":
                self.index_label = tk.Label(self.left_frame, text="Enter Index:", font=("Times New Roman", 14))
                self.index_label.pack(pady=(10, 5), padx=20)
                self.index_entry = tk.Entry(self.left_frame, font=("Times New Roman", 12))
                self.index_entry.pack(pady=(0, 10), padx=20)
             

            self.node_info_label = tk.Label(self.left_frame, text=label_text, font=("Times New Roman", 14))
            self.node_info_label.pack(pady=(10, 5), padx=20)

            self.node_info_entry = tk.Entry(self.left_frame, font=("Times New Roman", 12))
            self.node_info_entry.pack(pady=(0, 10), padx=20)
            if hasattr(self, 'confirm'):
                self.confirm.pack_forget()
                self.confirm = tk.Button(self.left_frame, text="Confirm", font=("Arial", 12), command=self.execute_method)
                self.confirm.pack(pady=(10, 20), padx=20)
            
        else:
            self.confirm.pack_forget()
            pass
                
      

    
    def execute_method(self):
        selected_structure = self.display_to_key[self.option.get()]
        selected_method = self.method.get()
    
        if selected_structure == "LinkedList":
            if selected_method == "Add":
                data = self.node_info_entry.get()
                self.ll_visualizer.animate_add(self.linked_list, data)
            elif selected_method == "Delete":
                if self.linked_list.head:
                    data = self.node_info_entry.get()
                    self.ll_visualizer.animate_delete(self.linked_list, data)

            elif selected_method == "Insert":
                if self.linked_list.length <= 0 or self.linked_list.length<self.index_entry.get():
                    print("Out of range")
                else:
                    data = self.node_info_entry.get()
                    self.ll_visualizer.animate_insert(self.linked_list, self.index_entry.get(), data)
            elif selected_method == "Reverse":
                self.ll_visualizer.animate_reverse(self.linked_list)
            elif selected_method == "Sort":
                self.ll_visualizer.animate_sort(self.linked_list)
            elif selected_method == "View":
                self.ll_visualizer.draw_list(self.linked_list)  # Add this line
            elif selected_method == "Generate":
                self.length = self.node_info_entry.get()
                self.ll_visualizer.animate_generate_random_list(self.linked_list, self.length)
        else:
            # Placeholder for other data structures
            print(f"Executing {selected_method} on {selected_structure}")
        

    def theme_switch(self):
        self.current_mode = "dark" if self.current_mode == "light" else "light"
        self.apply_theme()

    def update_methods(self, selected_display_option):
        selected_key = self.display_to_key[selected_display_option]
        methods = self.methods.get(selected_key, [])
        print(f"Methods for {selected_display_option} ({selected_key}):", methods)

        self.method_menu['values'] = methods
        
        if methods:
            self.method.set(methods[0])
        else:
            self.method.set("No methods available")
        
        # Call display_node_info whenever the method changes
        self.display_node_info()

        self.method.trace('w', lambda *args: self.display_node_info())    

    def apply_theme(self):
        theme = self.color_schemes[self.current_mode]
        
        self.master.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        self.left_frame.configure(bg=theme["bg"])
        self.right_frame.configure(bg=theme["bg"])
        self.data_structure_label.config(bg=theme["bg"], fg=theme["fg"])
        self.method_label.config(bg=theme["bg"], fg=theme["fg"])
        self.background_toggler.config(bg=theme["button"], fg=theme["fg"], activebackground=theme["accent"])
        self.confirm.config(bg=theme["button"], fg=theme["fg"], activebackground=theme["accent"])
        self.divider.config(bg=theme["fg"])  # Divider color is opposite of background
        self.canvas.config(bg="white" if self.current_mode == "light" else "#1E1E1E")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=theme["button"], background=theme["button"], foreground=theme["fg"])
        style.map('TCombobox', fieldbackground=[('readonly', theme["button"])], selectbackground=[('readonly', theme["accent"])], selectforeground=[('readonly', theme["fg"])])

if __name__ == "__main__":
    root = tk.Tk()
    app = DataStructureVisualizer(root)
    root.mainloop()