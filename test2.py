from ttkbootstrap import Style
from tkinter import ttk

style = Style()

window = style.master
window.geometry('600x400')
ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)
ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)
window.mainloop()