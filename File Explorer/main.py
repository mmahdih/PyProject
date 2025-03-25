from shutil import disk_usage
from tkinter import *
import customtkinter as ctk
from customtkinter import *
import psutil
import os
import string
from ctypes import windll
from PIL import ImageTk, Image
import numpy as np


# the Main window
class Window:
    def __init__(self, width, height, app):
        self.width = width
        self.height = height
        self.app = app
        self.app.title("File Explorer")
        self.app.geometry(f"{width}x{height}")
        self.app.resizable(True, True)


# make the main window
this_pc = Window(600, 400, CTk())

def enter(frame):
    # print("Entered the frame")
    frame.configure( border_width=2, border_color="lightblue", fg_color="#4c566a")

def exit_(frame):
    # print("Exited the frame")
    frame.configure(fg_color="#434c5e", border_width=0, corner_radius=10)



# def make_drive_frames(drive):
#     drive_frame = CTkFrame(this_pc.app)
#     drive_frame.grid(row=0, column=drives.index(drive), pady=10, padx=10, sticky="nw")
#     # drive_frame.pack(side=LEFT, pady=10, padx=10)
#
#     # drive sizes
#     total, used, free = disk_usage(drive)
#     drives_sizes[drive] = {"total": total, "used": used, "free": free}
#
#     # Create a frame for the icon and details within the drive_frame
#     icon_frame = CTkFrame(drive_frame)
#     icon_frame.grid(row=0, column=0, rowspan=3, sticky="nw")
#     # icon_frame.grid(row=0, column=0, rowspan=3)  # Corrected grid placement
#
#     detail_frame = CTkFrame(drive_frame)
#     detail_frame.grid(row=0, column=1, rowspan=3, sticky="nw")
#
#     # add an icon for each drive
#     png_img = Image.open("images\\hdd_white.PNG")
#     png_img = png_img.resize([60, 60])  # Resize the image
#
#     # Convert the image into a CTkImage object
#     drive_img = ctk.CTkImage(png_img, size=(60, 60))
#
#
#     # Create the label with the CTkImage object
#     label = ctk.CTkLabel(icon_frame, image=drive_img, text="")
#     label.grid(row=0, column=0, sticky="nw")
#
#     # Keep a reference to the image to prevent garbage collection
#     label.image = drive_img
#
#     # Drive label
#     drive_label = CTkLabel(detail_frame, text=f"{drive}:")
#     drive_label.grid(row=0, column=0, sticky="nw")
#     # drive_label.grid(row=0, column=0)
#
#     # Progress bar
#     drive_progress_bar = CTkProgressBar(detail_frame)
#     drive_progress_bar.set(drives_sizes[drive]["used"] / drives_sizes[drive]["total"])
#     drive_progress_bar.grid(row=1, column=0, sticky="nw")
#     # drive_progress_bar.grid(row=1, column=0)
#
#     # Drive usage label
#     drive_usage = CTkLabel(detail_frame, text=f"{free} GB free of {total} GB")
#     drive_usage.grid(row=2, column=0, pady=10, sticky="nw")
#     # drive_usage.grid(row=2, column=0, pady=10)
#
#     # Open drive button
#     # drive_button = CTkButton(drive_frame, text="Open Drive", command=lambda d=drive: open_file(f"{d}:"))
#     # drive_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="nw")
#
#     # Bind left-click event to open the drive
#     drive_frame.bind("<Button-1>", command=lambda d=drive: open_file(f"{drive}:"))
#
#
def make_drive_frames(drive):
    drive_frame = CTkFrame(this_pc.app, width=280, fg_color="#434c5e", border_width=0, corner_radius=10)
    drive_frame.grid(row=0, column=drives.index(drive), pady=10, padx=10, sticky="nw")
    # drive_frame.pack(side=LEFT, pady=10, padx=10)



    # drive sizes
    total, used, free = disk_usage(drive)
    drives_sizes[drive] = {"total": total, "used": used, "free": free}

    # add an icon for each drive
    png_img = Image.open("images\\hdd_white.PNG")
    png_img = png_img.resize([60, 60])  # Resize the image

    # Convert the image into a CTkImage object
    drive_img = ctk.CTkImage(png_img, size=(60, 60))

    # Create the label with the CTkImage object
    label = ctk.CTkLabel(drive_frame, image=drive_img, text="")
    label.grid(row=0, column=0, rowspan=3, sticky="nw", padx=5, pady=(10, 0))

    # Keep a reference to the image to prevent garbage collection
    label.image = drive_img

    my_font = ctk.CTkFont(family=("Helvetika"), size=22, weight="bold")

    # Drive label
    name = ""
    if (drive == "C"):
        name = f"{drive}: Windows"
    elif (drive == "D"):
        name = f"{drive}: Personal Files"

    drive_label = CTkLabel(drive_frame, text=name, font=my_font)
    drive_label.grid(row=0, column=1, sticky="nw", pady=(2,5))

    # Progress bar
    drive_progress_bar = CTkProgressBar(drive_frame, height=18, corner_radius=0)
    drive_progress_bar.set(drives_sizes[drive]["used"] / drives_sizes[drive]["total"])
    drive_progress_bar.grid(row=1, column=1, sticky="nw", padx=(0,10))

    # Drive usage label
    drive_usage = CTkLabel(drive_frame, text=f"{free} GB free of {total} GB")
    drive_usage.grid(row=2, column=1, pady=(5,2), sticky="nw")

    # Bind left-click event to open the drive
    drive_frame.configure(cursor="hand2")
    drive_frame.bind("<Button-1>", lambda d=drive: open_file(f"{drive}:"))
    label.bind("<Button-1>", lambda d=drive: open_file(f"{drive}:"))
    drive_label.bind("<Button-1>", lambda d=drive: open_file(f"{drive}:"))
    drive_usage.bind("<Button-1>", lambda d=drive: open_file(f"{drive}:"))
    drive_progress_bar.bind("<Button-1>", lambda d=drive: open_file(f"{drive}:"))

    drive_frame.bind('<Enter>', lambda event: enter(drive_frame))
    label.bind('<Enter>', lambda event: enter(drive_frame))
    drive_label.bind('<Enter>', lambda event: enter(drive_frame))
    drive_usage.bind('<Enter>', lambda event: enter(drive_frame))
    drive_progress_bar.bind('<Enter>', lambda event: enter(drive_frame))

    drive_frame.bind('<Leave>', lambda event: exit_(drive_frame))
    label.bind('<Leave>', lambda event: exit_(drive_frame))
    drive_label.bind('<Leave>', lambda event: exit_(drive_frame))
    drive_usage.bind('<Leave>', lambda event: exit_(drive_frame))
    drive_progress_bar.bind('<Leave>', lambda event: exit_(drive_frame))


# get the drives letter and return it
def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

drives = get_drives()
print(f"Drives: {drives}")

# get the disk usage of the hard drive
def disk_usage(drive_letter):
    hdd = psutil.disk_usage(f"{drive_letter}:")

    total = round(hdd.total / 1024 / 1024 / 1024, 2)
    used = round(hdd.used  / 1024 / 1024 / 1024, 2)
    free = round(hdd.free  / 1024 / 1024 / 1024, 2)

    print(f"DISK Total: {total} GB")
    print(f"Disk Used: {used} GB")
    print(f"Disk Free: {free} GB")

    return total, used, free

def open_file(file_path):
    # os.startfile(file_path)
    dir_frame = CTkFrame(this_pc.app, width=280)

    for file in load_files(file_path):
        print(file)
        button = CTkButton(dir_frame, text=file, command=lambda file=file: open_file(f"{file_path}:\\{file}"))
        button.pack(pady=10)

    print(f"Opening file: {file_path}")
    print(load_files(file_path))

def load_files(file_path):
    files = os.listdir(f"{file_path}\\")
    return files

drives_sizes = {}

# make a frame for every drive in this pc
for drive in drives:
    print(f"Drive: {drive}")

    # Create the parent frame for the drive
    make_drive_frames(drive)





if __name__ == "__main__":
    this_pc.app.mainloop()


















# CPU
def cpu_usage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

# RAM
def ram_usage():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent














class MyFrame(CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.pack()

# my_img = Image.open('images/ssd.png')
# # Create a CTkLabel widget to display the image
# my_label = ctk.CTkLabel(drive_frame, image=my_img, text="")
# my_label.pack()
#
# # Keep a reference to the image to prevent garbage collection
# my_label.image = my_img

# drive = MyFrame(this_pc.app, 300, 400)
# drive.pack(side=LEFT)
#
# frame2 = MyFrame(this_pc.app, 300, 400)
# frame2.pack(side=RIGHT)


# get the size of the files
# file_size = os.path.getsize('images\\hdd.png')
# in_kb = file_size / 1024
# in_kb = round(in_kb, 2)
# print(in_kb)





