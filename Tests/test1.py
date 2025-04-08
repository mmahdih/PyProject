import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttb
from ttkbootstrap import Style
from ttkbootstrap.constants import *

# Create a root window with ttkbootstrap
root = ttb.Window()
root.title("My Application")

# Apply the "superhero" theme
style = Style(theme="superhero")

button = ttk.Button(root, text="Click Me").pack()

# default label style
ttb.Label(text="test").pack()

# danger colored label style
ttb.Label(text = "text",bootstyle="danger.Inverse").pack()



# Start the main loop
root.mainloop()