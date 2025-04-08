import tkinter as tk
import customtkinter as ctk

# Create the root window using CustomTkinter
root = ctk.CTk()

# Set window title and size
root.title("Main Window with CTk and Tk Widgets")
root.geometry("400x300")

# Add a CustomTkinter button
button_ctk = ctk.CTkButton(root, text="CustomTkinter Button")
button_ctk.pack(pady=20)

# Add a Tkinter label (standard Tk widget)
label_tk = tk.Label(root, text="This is a Tkinter Label")
label_tk.pack(pady=10)

# Add a Tkinter button (standard Tk widget)
button_tk = tk.Button(root, text="This is a Tkinter Button")
button_tk.pack(pady=10)

# Run the main loop
root.mainloop()
