from tkinter import *
from customtkinter import *
import psutil
import os


# load all files in C:\
def load_files():
    files = os.listdir("C:\\")
    return files





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

print(f"CPU Usage: {cpu_usage()}%")
print(f"RAM Usage: {ram_usage()}%")
print(f"DISK Usage: {disk_usage()}%")



class Windows:
    def __init__(self, width, height, app):
        self.width = width
        self.height = height
        self.app = app
        self.app.title("File Explorer")
        self.app.geometry(f"{width}x{height}")
        self.app.resizable(False, False)

    def button(self, text, command):
        button = CTkButton(self.app, text=text, command=command, fg_color="green", corner_radius=10)
        button.pack(pady=10)

    def progressBar(self, value):
        progress_bar = CTkProgressBar(self.app)
        progress_bar.set(value)
        progress_bar.pack(pady=10)



main_explorer_window = Windows(600, 400, CTk())
main_explorer_window.button("Load Files", disk_usage())
main_explorer_window.progressBar((cpu_usage())/100)
main_explorer_window.progressBar((ram_usage())/100)
main_explorer_window.progressBar((disk_usage())/100)
main_explorer_window.app.mainloop()
