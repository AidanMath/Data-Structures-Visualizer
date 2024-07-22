import tkinter as tk
from tkinter import ttk
import random
import LinkedList, Array, HashTable, Queue, Stack, BinaryTree
import ast
class DataStructureVisualizer:
    def __init__(self, master):
        self.master = master # OG window
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
        self.background_toggler = tk.Button(self.master, text="Toggle Theme", command=self.theme_switch)
        self.background_toggler.pack(side="top", anchor="nw")

        # Data structure selection
        self.data_structure_label = tk.Label(master, text="Select Data Structure to Visualize:", font=("Times New Roman", 18, "bold"))
        self.data_structure_label.pack(pady=20)

        self.option = tk.StringVar()
        self.option.set("Arrays")
        self.options = ["Arrays", "Binary Tree", "Linked List", "Stack", "Queue", "Hashing Table"]
        
    
        self.dropdown = tk.OptionMenu(master, self.option, *self.options)

        self.method = tk.StringVar()
        self.methods = self.read_dict()
        self.method.set(self.methods.keys()[0])
        
    
        self.method_menu = tk.OptionMenu(master, self.method, self.methods.keys())
        self.method_menu.pack(pady=10)

       
        self.update_methods(self.option.get()) 

        
    
        
        # Styling
        self.dropdown.config(
            bg="white",  
            fg="black",      
            font=("Arial", 12),  
            width=20,        
            highlightthickness=2,  
            highlightbackground="black",
            activebackground="white",  
        )
       
        self.dropdown["menu"].config(
            bg="white",
            fg="black",
            activebackground="lightblue",
            activeforeground="black",
            font=("Arial", 12)
        )
    
        self.dropdown.pack(padx=10, side="top")

        self.apply_theme()
    
    
    def update_methods(self, selected_option):
     
        menu = self.method_menu['menu']
        menu.delete(0, 'end')

        methods = self.methods.get(selected_option, [])
        for method in methods:
            menu.add_command(label=method, command=tk._setit(self.method, method))
        if methods:
            self.method.set(methods[0])
        else:
            self.method.set("No methods available")

    def read_dict(self):
        file_path="Data Stuctures  python/methods.txt"
        with open(file_path, 'r') as file:
            file_contents=file.read()
        result=ast.literal_eval(file_contents)
        return result
    
    





    def theme_switch(self):
        self.current_mode = "dark" if self.current_mode == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = self.color_schemes[self.current_mode]
        
        self.master.configure(bg=theme["bg"])
        self.data_structure_label.config(bg=theme["bg"], fg=theme["fg"])
        self.background_toggler.config(bg=theme["button"], fg=theme["fg"], activebackground=theme["accent"])
        
        # Changes styling 
        self.dropdown.config(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["accent"],
            highlightbackground=theme["fg"]
        )
        
        self.dropdown["menu"].config(
            bg=theme["button"],
            fg=theme["fg"],
            activebackground=theme["accent"],
            activeforeground=theme["fg"]
        )

root = tk.Tk()
app = DataStructureVisualizer(root)
root.mainloop()