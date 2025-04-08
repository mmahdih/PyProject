import datetime
import os
import tkinter as tk
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



selected_items = []

# the Main window
class Window:
    def __init__(self, width, height, app):
        x = (app.winfo_screenwidth() - width) // 2
        y = (app.winfo_screenheight() - height) // 2

        self.width = width
        self.height = height
        self.app = app
        self.app.title("File Explorer")
        self.app.geometry(f"{width}x{height}+{x}+{y}")
        # self.app.attributes("-topmost", True)

    def fullscreen_toggle(self):
        self.app.attributes("-fullscreen", not self.app.attributes("-fullscreen"))


# make the main window
this_pc = Window(1500, 800, ttk.Window(themename="superhero"))


def copy():
    # global selected_items
    print(selected_items)
    # print(dir_history.get_current_dir())



def cut(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())

def rename(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())

def delete(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())

def paste(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())

def new_folder(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())


def new_file(event):
    global selected_items
    print(selected_items)


def milsec_to_time(milsec):
    return str(datetime.timedelta(seconds=milsec // 1000))





def open_file():
    print("opening file")
    file_stats = os.stat(selected_items[0])
    print(file_stats)
    creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
    modification_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
    last_access_time = datetime.datetime.fromtimestamp(file_stats.st_atime)
    permission = oct(file_stats.st_mode)


    print(f"Creation Time: {creation_time}")
    print(f"Modification Time: {modification_time}")
    print(f"Last Access Time: {last_access_time}")
    print(f"Permission: {permission}")
    print("opening the selected item")
    for i in selected_items:
        if not i.endswith(".png"):
            continue
        os.startfile(i)
        print(i)
    print("open complete")
    selected_items.clear()




toolbar = ttk.Frame(this_pc.app, height=30)
toolbar.pack(side=TOP, fill=X, ipady=10, ipadx=10)

class ToolbarButton(ttk.Button):
    def __init__(self, master, image_path, command, **kwargs):
        img = ImageTk.PhotoImage(Image.open(image_path).resize((25, 25)))
        super().__init__(master, image=img,  command=command, **kwargs)
        self.image = img

back_btn = ToolbarButton(toolbar, "images\\back.png_white.png", lambda: back(), style="Outline.TButton")
back_btn.pack(side=LEFT, padx=10)

forward_btn = ToolbarButton(toolbar, "images\\forward.png_white.png", lambda: print("forward"), style="Outline.TButton")
forward_btn.pack(side=LEFT, padx=10)

navigation_pane_btn = ToolbarButton(toolbar, "images\\navigation_pane.png_white.png", lambda: print("navigation pane"), style="Outline.TButton")
navigation_pane_btn.pack(side=LEFT, padx=10)

preview_pane_btn = ToolbarButton(toolbar, "images\\preview_pane.png_white.png", lambda: print("preview pane"), style="Outline.TButton")
preview_pane_btn.pack(side=LEFT, padx=10)

copy_btn = ToolbarButton(toolbar, "images\\copy.png_white.png", command=lambda: open_file(), style="Outline.TButton")
copy_btn.pack(side=LEFT, padx=10)

cut_btn = ToolbarButton(toolbar, "images\\cut.png_white.png", lambda: print("cut"), style="Outline.TButton")
cut_btn.pack(side=LEFT, padx=10)

paste_btn = ToolbarButton(toolbar, "images\\paste.png_white.png", lambda: print("paste"), style="Outline.TButton")
paste_btn.pack(side=LEFT, padx=10)

rename_btn = ToolbarButton(toolbar, "images\\rename.png_white.png", lambda: print("rename"), style="Outline.TButton")
rename_btn.pack(side=LEFT, padx=10)

delete_btn = ToolbarButton(toolbar, "images\\delete.png_white.png", lambda: print("delete"), style="Outline.TButton")
delete_btn.pack(side=LEFT, padx=10)

new_folder_btn = ToolbarButton(toolbar, "images\\new_folder.png_white.png", lambda: print("new folder"), style="Outline.TButton")
new_folder_btn.pack(side=LEFT, padx=10)
# # selection pane
selection_pane = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=1, corner_radius=0, height=30)
selection_pane.pack(side=BOTTOM, fill=X)

main_panel = ttk.PanedWindow(this_pc.app,  orient=HORIZONTAL)
main_panel.pack(side=LEFT, fill=BOTH, expand=1)

navigation_pane = ttk.PanedWindow(main_panel, width=250)
main_panel.add(navigation_pane)




folder_img = tk.PhotoImage(file="images\\folder_color 20.png")
file_img = tk.PhotoImage(file="images\\file_color_20.png")

middle_pane = ttk.PanedWindow(main_panel,  width=1000, orient=VERTICAL)
main_panel.add(middle_pane)


middle_pane.bind("<BackSpace>", lambda event: print("backspace clicked"))
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
tabletree.column("File Type", width=100, anchor="center", stretch=FALSE)
tabletree.column("Date Created", width=150, anchor="center", stretch=FALSE)
tabletree.column("Date Modified", width=150, anchor="center", stretch=FALSE)
tabletree.column("Size", width=100, anchor="e", stretch=FALSE)

tabletree.heading("#0", text="", )
tabletree.heading("Name", text="Name", anchor="w")
tabletree.heading("File Type", text="File Type")
tabletree.heading("Date Created", text="Date Created")
tabletree.heading("Date Modified", text="Date Modified")
tabletree.heading("Size", text="Size")

tabletree.pack(side=LEFT, fill=BOTH, expand=1)


def item_select(_):
    # print("Double Click")
    # print(tabletree.selection())
    for i in tabletree.selection():
        # print(tabletree.item(i)["values"][0])
        if tabletree.item(i)["values"][1] == "File":
            print("Files")
            os.startfile(f"{dir_history.get_current_dir()}\\{tabletree.item(i)['values'][0]}")
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




# tabletree.bind("<<TreeviewSelect>>", item_select)
tabletree.bind('<ButtonRelease-1>', single_click)
tabletree.bind('<Double-1>', item_select)

preview_pane = ttk.PanedWindow(main_panel, width=250)
main_panel.add(preview_pane)

label2 = ttk.Label(preview_pane, text="Preview Pane")
preview_pane.add(label2)


# the directory history
class DirectoryHistory:
    def __init__(self):
        self.history = []

    def change_dir(self, new_dir):
        self.history.append(new_dir)
        delimiter = '\\'
        joined = delimiter.join(self.history)
        print(f"History: {joined}")

        print(f"Changing directory to: {new_dir}")

        self.current_dir = joined

        print(f"Current Directory: {self.current_dir}")
        return self.current_dir

    def go_back(self):
        if len(self.history) > 0:
            self.history.pop()
            delimiter = '\\'
            joined = delimiter.join(self.history)
            self.current_dir = joined
        else:
            print("No previous directory available")

        print(f"Current Directory: {self.current_dir}")

        return self.current_dir

    def get_current_dir(self):
        return self.current_dir

    def clear_history(self):
        self.history = []

    def set_initial_dir(self, initial_dir):
        self.current_dir = initial_dir
        self.history.append(initial_dir)


dir_history = DirectoryHistory()

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


# def enter(frame):
#     frame.configure(border_width=2, border_color="lightblue", fg_color="#4c566a")
#
#
# def exit_(frame):
#     frame.configure(fg_color="#434c5e", border_width=0, corner_radius=10)


def initial_dir(dir_name):
    dir_history.clear_history()
    dir_history.set_initial_dir(dir_name)
    print("Initial Directory:", dir_name)
    tabletree.delete(*tabletree.get_children())
    open_dir(dir_name)


def change_dir(dir_name):
    print("Current Directory: B: ", dir_history.get_current_dir())
    new_dir = dir_history.change_dir(dir_name)
    print("Current Directory: A: ", dir_history.get_current_dir())
    tabletree.delete(*tabletree.get_children())
    open_dir(new_dir)


def back():
    print("Current Directory: B: ", dir_history.get_current_dir())
    new_dir = dir_history.go_back()
    print("Current Directory: A: ", dir_history.get_current_dir())
    tabletree.delete(*tabletree.get_children())
    open_dir(new_dir)


def make_drive_frames(drive):
    # Create a frame with improved style
    drive_frame = ttk.Frame(navigation_pane, style="primary.TFrame", width=300, height=100)
    navigation_pane.add(drive_frame)

    # Grid configuration with more spacing
    drive_frame.grid(row=drives.index(drive), column=0, pady=15, padx=20, sticky="nsew")

    # Get disk usage
    total, used, free = disk_usage(drive[0])
    drives_sizes[drive[0]] = {"total": total, "used": used, "free": free}

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
    drive_frame.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_usage.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_progress_bar.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))

    # drive_frame.bind('<Enter>', lambda event: drive_frame.configure(style="primary.TButton"))
    # label.bind('<Enter>', lambda event: drive_frame.configure(style="primary.TButton"))
    # drive_label.bind('<Enter>', lambda event: drive_frame.configure(style="primary.TButton"))
    # drive_usage.bind('<Enter>', lambda event: drive_frame.configure(style="primary.TButton"))
    # drive_progress_bar.bind('<Enter>', lambda event: drive_frame.configure(style="primary.TButton"))
    #
    # drive_frame.bind('<Leave>', lambda event: exit_(drive_frame))
    # label.bind('<Leave>', lambda event: exit_(drive_frame))
    # drive_label.bind('<Leave>', lambda event: exit_(drive_frame))
    # drive_usage.bind('<Leave>', lambda event: exit_(drive_frame))
    # drive_progress_bar.bind('<Leave>', lambda event: exit_(drive_frame))




def get_drives_info():
    # List all logical drives
    partitions = psutil.disk_partitions()
    print(f"Partitions: {partitions}")
    drives = []

    # Filter out partitions that have no media (skip 'no media' drives)
    for partition in partitions:
        # Check if the partition is mounted and has a valid device
        if partition.fstype and partition.device != '::':
            try:
                drives_info = win32api.GetVolumeInformation(partition.mountpoint)
                drives.append([partition.mountpoint, drives_info[0]])
            except Exception as e:
                print(f"Error getting volume information for {partition.mountpoint}: {e}")
    print(drives)
    return drives


# get the disk usage of the hard drive
def disk_usage(drive_letter):
    hdd = psutil.disk_usage(drive_letter)

    total = round(hdd.total / 1024 / 1024 / 1024, 2)
    used = round(hdd.used / 1024 / 1024 / 1024, 2)
    free = round(hdd.free / 1024 / 1024 / 1024, 2)

    print(f"DISK Total: {total} GB")
    print(f"Disk Used: {used} GB")
    print(f"Disk Free: {free} GB")

    return total, used, free



def get_file_size(file_path):
    file_stats = os.stat(file_path)

    # file size in bytes
    bytes = file_stats.st_size

    # convert bytes to KB
    kb = bytes / 1024

    # round to 2 decimal places
    kb = round(kb, 0)

    print(f"File size: {kb} KB")

    # convert bytes to MB
    mb = bytes / 1024 / 1024

    # round to 2 decimal places
    mb = round(mb, 3)

    print(f"File size: {mb} MB")

    #

    if kb < 1024:
        return f"{kb} KB"
    else:
        return f"{mb} MB"


def open_dir(file_path):
    # this is how th file path looks like: ['C:\\', 'Windows']
    print(f"Opening dir: {file_path}")

    for file in load_files(file_path):
        file_dir = f"{dir_history.get_current_dir()}/{file}"

        file_stats = os.stat(file_dir)
        print(file_stats)
        creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
        modification_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
        last_access_time = datetime.datetime.fromtimestamp(file_stats.st_atime)
        file_size = get_file_size(file_dir)
        # file_size = f"{round(file_stats.st_size / 1024, 2)} KB"

        permission = oct(file_stats.st_mode)

        if os.path.isfile(file_dir):
            tabletree.insert("", index=tk.END, values=(file, "File", creation_time, modification_time, file_size), image=file_img)
        if os.path.isdir(file_dir):
            tabletree.insert("", index=tk.END, values=(file, "Folder",creation_time, modification_time, ""), image=folder_img)


def load_files(file_path):
    print(f"loading: {file_path}")
    files = os.listdir(file_path)
    return files


drives_sizes = {}

drives = get_drives_info()
# make a frame for every drive in this pc
for drive in drives:
    print(drive)
    # Create the parent frame for the drive
    make_drive_frames(drive)

if __name__ == "__main__":
    this_pc.app.mainloop()
