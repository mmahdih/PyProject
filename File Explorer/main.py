from tkinter import *
from tkinter import ttk
import psutil


# CPU

def cpu_usage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent


# RAM

def ram_usage():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent  

# DISK

def disk_usage():
    disk_percent = psutil.disk_usage('/').percent
    return disk_percent

print (cpu_usage(), ram_usage(), disk_usage())



class Windows:
    def __init__(self, width, height, root):
        self.width = width
        self.height = height
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
        self.root.config(bg="white")
        self.root.mainloop()
        
        
main_explorer_window = Windows(600, 400, Tk())

