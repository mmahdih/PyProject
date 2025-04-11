import datetime
import os
from ensurepip import bootstrap
from tkinter import Canvas

import ttkbootstrap
# import tkinter as tk
import ttkbootstrap as ttk
from Cython.Utils import modification_time
from ttkbootstrap.constants import *
import customtkinter as ctk
from customtkinter import *
from shutil import disk_usage
import psutil
import win32api
from PIL import Image, ImageTk
from pywin.framework.help import helpIDMap
from ttkbootstrap.icons import Icon
from uri_template import expand

# my packges
from Utils.functions import *
from Utils.folders_tree import *
from Utils.classes import *
from gui_components.folders import *
from gui_components.preview_pane import *
from gui_components.navigation_pane import *
from gui_components.toolbar import *



selected_items = []

# make the main window with superhero theme
this_pc = Window(1500, 800, ttkbootstrap.Window(themename="superhero"))

# Dir History
dir_history = DirectoryHistory()

folder_img = tk.PhotoImage(file="images\\folder_color 20.png")
file_img = tk.PhotoImage(file="images\\file_color_20.png")


# Define toolbar buttons and their commands
toolbar_commands = [
    ("images\\back.png_white.png", lambda: back()),
    ("images\\forward.png_white.png", lambda: print("forward")),
    ("images\\navigation_pane.png_white.png", lambda: print("navigation_pane")),
    ("images\\preview_pane.png_white.png", lambda: print("preview pane")),
    ("images\\copy.png_white.png", lambda: open_file(selected_items)),
    ("images\\cut.png_white.png", lambda: print("cut")),
    ("images\\paste.png_white.png", lambda: print("paste")),
    ("images\\rename.png_white.png", lambda: print("rename")),
    ("images\\delete.png_white.png", lambda: print("delete")),
    ("images\\new_folder.png_white.png", lambda: print("new folder"))
]

# Create the toolbar, selection pane, and main panel
toolbar = create_toolbar(this_pc.app, toolbar_commands)
selection_pane = create_selection_pane(this_pc.app)
main_panel = create_main_panel(this_pc.app)
navigation_pane = create_navigation_pane(main_panel)
middle_pane = create_middle_pane(main_panel)
preview_pane = create_preview_pane(main_panel)


# Function to sort the Treeview by column
def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


tabletree = ttk.Treeview(middle_pane)
vsb = ttk.Scrollbar(middle_pane, orient="vertical", command=tabletree.yview)

vsb.pack(side=RIGHT, fill=Y)
hsb = ttk.Scrollbar(middle_pane, orient="horizontal", command=tabletree.xview)
hsb.pack(side=BOTTOM, fill=X)
tabletree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tabletree.tag_configure("large", font=("arial", 16))
tabletree["columns"] = ("Name", "File Type", "Date Created", "Date Modified" , "Size")

tabletree.column("#0", width=40, minwidth=40, stretch=FALSE)
tabletree.column("Name", width=200, stretch=FALSE)
tabletree.column("File Type", width=100, anchor="w", stretch=FALSE)
tabletree.column("Date Created", width=150, anchor="w", stretch=FALSE)
tabletree.column("Date Modified", width=150, anchor="w", stretch=FALSE)
tabletree.column("Size", width=100, anchor="e", stretch=FALSE)

tabletree.heading("#0", text="" )
tabletree.heading("Name", text="Name", anchor="w")
tabletree.heading("File Type", text="File Type")
tabletree.heading("Date Created", text="Date Created")
tabletree.heading("Date Modified", text="Date Modified")
tabletree.heading("Size", text="Size")

tabletree.pack(side=LEFT, fill=BOTH, expand=1)


def double_click(_):
    # print("Double Click")
    # print(tabletree.selection())
    for i in tabletree.selection():
        # print(tabletree.item(i)["values"][0])
        if tabletree.item(i)["values"][1] in ["png", "jpg", "jpeg"]:
            print("Files")
            # os.startfile(f"{dir_history.get_current_dir()}\\{tabletree.item(i)['values'][0]}")

            create_photo_viewer(tabletree.item(i)['values'][0])
        elif tabletree.item(i)["values"][1] == "Folder":
            change_dir(tabletree.item(i)["values"][0])



def single_click(_):
    # print("Single Click")
    # print(tabletree.selection())
    for i in tabletree.selection():
        print(tabletree.item(i)["values"][0])
        file_dir = f"{dir_history.get_current_dir()}\\{tabletree.item(i)['values'][0]}"
        print(file_dir)
        selected_items.append(file_dir)

# tabletree.bind("<<TreeviewSelect>>", double_click)
tabletree.bind('<ButtonRelease-1>', single_click)
tabletree.bind('<Double-1>', double_click)


# Add elements to the preview pane
label2 = ttk.Label(preview_pane, text="Preview Pane")
preview_pane.add(label2)



def next_image(all_images, current_image_position):
    print("Next Image")
    create_photo_viewer(all_images[(current_image_position + 1) % len(all_images)])


def previous_image(all_images, current_image_position):
    print("Previous Image")
    create_photo_viewer(all_images[(current_image_position - 1) % len(all_images)])


def create_photo_viewer(image):
    for widget in preview_pane.winfo_children():
        print(f"Widget: {widget}")
        widget.destroy()

    image_dir = f"{dir_history.get_current_dir()}\\{image}"
    print(f"Image dir: {image_dir}")

    try:
        image_import = Image.open(image_dir)
    except IOError:
        print(f"Error: Could not load image {image}")
        return

    image_ratio = image_import.size[0] / image_import.size[1]
    print("image Ratio: %s" % image_ratio)
    image_tk = ImageTk.PhotoImage(image_import)
    if image_tk is None:
        print(f"Error: Could not load image {image}")
        return

    print(f"Image {image} loaded successfully")

    canvas = ctk.CTkCanvas(preview_pane, width=preview_pane.winfo_width() - 50, height=preview_pane.winfo_height() - 50)
    preview_pane.add(canvas)

    canvas.bind("<Configure>", lambda event, image=image_tk: resize_image(canvas, event, image_import, image_tk, image_ratio))
    canvas.image = image_tk

    all_images = [file for file in os.listdir(dir_history.get_current_dir()) if
                  file.lower().endswith(('.png', '.jpg', '.jpeg'))]


    # find the current iamge position
    if image in all_images:
        current_image_position = all_images.index(image)
        print(current_image_position)
    else:
        print("image not found")

    button_frame = ctk.CTkFrame(preview_pane)
    preview_pane.add(button_frame)

    next_image_button = ctk.CTkButton(button_frame, text="Next",
                                      command=lambda: next_image(all_images, current_image_position))
    next_image_button.pack(side=LEFT,  expand=True)

    prev_image_button = ctk.CTkButton(button_frame, text="Previous", command=lambda: previous_image(all_images, current_image_position))
    prev_image_button.pack(side=LEFT,  expand=True)

    if len(all_images) > 1:
        next_image_button.configure(state="normal")
        prev_image_button.configure(state="normal")
    else:

        next_image_button.configure(state="disabled")
        prev_image_button.configure(state="disabled")


def resize_image(canvas, event, image_import, image_tk, image_ratio):

    # current canvas ratio
    canvas_ratio = event.width / event.height
    print(f"canvas ratio: {canvas_ratio}")
    print(f"image ratio: {image_ratio}")

    if canvas_ratio > image_ratio:
        image_height = event.height
        image_width = int(image_height * image_ratio)
    else:
        image_width = event.width
        image_height = int(image_width / image_ratio)

    print(f"canvas size: {event.width} x {event.height}")
    print(f"image size: {image_width} x {image_height}")

    resized_image = image_import.resize((image_width, image_height))
    image_tk = ImageTk.PhotoImage(resized_image)

    canvas.delete("all")
    canvas.create_image(event.width / 2, event.height / 2, image=image_tk, anchor="center")
    canvas.image = image_tk



#     # Clear the previous frame
#     for widget in preview_pane.winfo_children():
#         widget.destroy()
#
#     photo_viewer_frame = ctk.CTkFrame(preview_pane, corner_radius=10, width=700, height=394)
#     preview_pane.add(photo_viewer_frame)
#
#     image_dir = f"{dir_history.get_current_dir()}\\{image}"
#     print(f"the image: {image_dir}")
#
#     # Get all images in the current directory with the .png .jpg .jpeg extension
#     all_images = [file for file in os.listdir(dir_history.get_current_dir()) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
#
#
#     # find the current iamge position
#     if image in all_images:
#         current_image_position = all_images.index(image)
#         print(current_image_position)
#     else:
#         print("image not found")
#
#     my_image = Image.open(image_dir)
#     print("test")
#     print(my_image)
#     width, height = my_image.size
#     print(f"width: {width}, height: {height}")
#
#     image_ratio = width / height
#     print(f"image ratio: {image_ratio}")
#
#     scale = min(700 / width, 394 / height)
#     new_width = int(width * scale)
#     new_height = int(height * scale)
#     the_image = ctk.CTkImage(my_image, size=(width / 2, height / 2))
#
#     # Create the label with the CTkImage object
#     label = ctk.CTkLabel(photo_viewer_frame, image=the_image, text="", bg_color="gray10")
#     label.place(relx=0.5, rely=0.5, anchor="center")
#
#     next_image_button = ctk.CTkButton(photo_viewer_frame, text="Next", command=lambda: next_image(all_images, current_image_position))
#     next_image_button.place(relx=0.8, rely=0.9, anchor="center")
#
#     prev_image_button = ctk.CTkButton(photo_viewer_frame, text="Previous", command=lambda: previous_image(all_images, current_image_position))
#     prev_image_button.place(relx=0.2, rely=0.9, anchor="center")
#
#
#     print(len(all_images))
#
#     if len(all_images) > 1:
#         next_image_button.configure(state="normal")
#         prev_image_button.configure(state="normal")
#     else:
#
#         next_image_button.configure(state="disabled")
#         prev_image_button.configure(state="disabled")
#
#     # Keep a reference to the image to prevent garbage collection
#     label.image = my_image
#
#     return photo_viewer_frame

# bind the F11 key to toggle fullscreen
this_pc.app.bind("<F11>", lambda event: this_pc.fullscreen_toggle())
if this_pc.app.state() != "normal":
    this_pc.app.bind("<Escape>", lambda event: this_pc.fullscreen_toggle())
print("state: ", this_pc.app.state())


def open_foto(name):
    this_pc.app.geometry("1500x600")
    global image_frame
    image_frame = ctk.CTkFrame(this_pc.app, width=700, height=394)
    image_frame.grid(row=0, column=3, rowspan=10, sticky="nsew", pady=10, padx=10)

    image_dir = f"{dir_history.get_current_dir()}\\{name}"
    print(image_dir)

    my_image = Image.open(image_dir)
    width, height = my_image.size
    scale = min(700 / width, 394 / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    the_image = ctk.CTkImage(my_image, size=(new_width, new_height))

    # Create the label with the CTkImage object
    label = ctk.CTkLabel(image_frame, image=the_image, text="")
    label.place(relx=0.5, rely=0.5, anchor="center")

    # Keep a reference to the image to prevent garbage collection
    label.image = my_image



def initial_dir(dir_name):
    dir_history.clear_history()
    dir_history.set_initial_dir(dir_name)
    print("Initial Directory:", dir_name)
    tabletree.delete(*tabletree.get_children())
    open_dir(dir_name, dir_history, tabletree, file_img, folder_img)


def change_dir(dir_name):
    print("Current Directory: B: ", dir_history.get_current_dir())
    new_dir = dir_history.change_dir(dir_name)
    print("Current Directory: A: ", dir_history.get_current_dir())
    tabletree.delete(*tabletree.get_children())
    open_dir(new_dir, dir_history, tabletree, file_img, folder_img)


def back():
    print("Current Directory: B: ", dir_history.get_current_dir())
    new_dir = dir_history.go_back()
    print("Current Directory: A: ", dir_history.get_current_dir())
    tabletree.delete(*tabletree.get_children())
    open_dir(new_dir, dir_history, tabletree, file_img, folder_img)


def make_drive_frames(drive):
    # Create a frame with improved style
    drive_frame = ttk.Frame(navigation_pane, style="primary.TFrame", width=300, height=100)
    navigation_pane.add(drive_frame)

    # Grid configuration with more spacing
    drive_frame.grid(row=drives.index(drive), column=0, pady=15, padx=20, sticky="nsew")

    # Get disk usage
    total, used, free = disk_usage(drive[0])

    drive_img = ImageTk.PhotoImage(Image.open("images\\hdd_white.png").resize((45,45)))

    # Create a label with the CTkImage object
    label = ttk.Label(drive_frame, image=drive_img, text="", style="primary.Inverse.TLabel")
    label.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=5, pady=(15, 0))

    # Keep a reference to the image to prevent garbage collection
    label.image = drive_img

    # Drive label with a more modern font and spacing
    drive_label = ttk.Label(drive_frame, text=drive[1], style="primary.Inverse.TLabel", font=("Helvetica", 14, "bold"))
    drive_label.grid(row=0, column=1, sticky="nsew", pady=(5, 0), padx=5)

    # Progress bar with a cleaner and more modern look using ttkbootstrap's styles
    drive_progress_bar = ttk.Progressbar(drive_frame, orient="horizontal", style="success.Horizontal.TProgressbar")
    drive_progress_bar.grid(row=1, column=1, sticky="nsew", pady=(5, 0), padx=(5, 10))
    drive_progress_bar['maximum'] = 100  # Set maximum value as percentage
    drive_progress_bar['value'] = (used / total) * 100  # Calculate the used percentage
    drive_progress_bar['length'] = 200  # Set a fixed length for consistency

    # Drive usage label with better font and spacing
    drive_usage = ttk.Label(drive_frame, text=f"{free} GB free of {total} GB", font=("Helvetica", 10),
                            style="primary.Inverse.TLabel")
    drive_usage.grid(row=2, column=1, sticky="nsew", pady=(5, 10), padx=5)


    # Bind left-click event to open the drive
    drive_frame.configure(cursor="hand2")
    print(f"drive before initialization: {drive}")
    def open_drive(event):
        initial_dir(f"{drive[0]}")
    for widget in (drive_frame, label, drive_label, drive_usage, drive_progress_bar):
        widget.bind("<Button-1>", open_drive)


drives = get_drives_info()
# make a frame for every drive in this pc
for drive in drives:
    print(drive)
    # Create the parent frame for the drive
    make_drive_frames(drive)

if __name__ == "__main__":
    this_pc.app.mainloop()
