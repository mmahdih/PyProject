import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()

# Load images using PhotoImage
image1 = tk.PhotoImage(file="File Explorer\\images\\folder_color.png").subsample(2,2)  # Make sure to provide the correct path to your image
image2 = tk.PhotoImage(file="File Explorer\\images\\folder_color.png").subsample(2,2)  # Similarly, provide the correct path

# Create a Treeview widget
tree = ttk.Treeview(root)

# Define columns
tree['columns'] = ("Name", "Age")
tree.column("#0", width=50)
tree.column("Name", width=200, anchor="w")
tree.column("Age", width=100)

# Define headings
tree.heading("#0", text="")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")

# Insert items with images
tree.insert("", "end", "#1", text="", values=("John", 25), image=image1)
tree.insert("", "end", "#2", text="", values=("Jane", 30), image=image2)

# Pack the treeview widget
tree.pack()

# Run the main loop
root.mainloop()
