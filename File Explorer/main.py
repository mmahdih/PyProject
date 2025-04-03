import tkinter as tk
from shutil import disk_usage
import ttkbootstrap as ttk
import customtkinter as ctk
import psutil
import win32api
from PIL import Image
from customtkinter import *

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
        self.app.attributes("-topmost", True)

    def fullscreen_toggle(self):
        self.app.attributes("-fullscreen", not self.app.attributes("-fullscreen"))


# make the main window
this_pc = Window(1500, 800, tk.Window())

class Make_Button(ctk.CTkButton):
    def __init__(self, parent, text, width, height, fg_color, hover_color, cursor, command, image=None, padx=0, pady=0):
        super().__init__(parent, text=text, command=command, width=width, height=height, fg_color=fg_color,
                         hover_color=hover_color, cursor=cursor, compound="left", border_width=0)

        if image is not None:
            image = "images\\" + image
            image = ctk.CTkImage(Image.open(image), size=(width, height))
            self.configure(image=image, compound="left")

        self.pack(side=LEFT, padx=padx, pady=pady)

    def img(self, image, width, height):
        image = "images\\" + image
        image = ctk.CTkImage(Image.open(image), size=(width, height))
        self.configure(image=image, compound="left")


def copy(event):
    global selected_items
    print(selected_items)
    print(dir_history.get_current_dir())


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




toolbar = ctk.CTkFrame(this_pc.app, fg_color="lightblue", border_width=1, corner_radius=0, height=30)
toolbar.pack(side=TOP, fill=X, ipady=10, ipadx=10)

back_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: back(), "back.png", padx=(10, 1))
back_btn.configure(corner_radius=5)

forward_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("forward"), "forward.png")
forward_btn.configure(corner_radius=5)

navigation_pane_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("preview pane"),
                                  "navigation_pane.png", padx=10)
navigation_pane_btn.configure(corner_radius=5)



# preview pane toolbar button
preview_pane_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("preview pane"),
                               "preview_pane.png", padx=10)
preview_pane_btn.configure(corner_radius=5)

copy_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("copy"), "copy.png", padx=10)
copy_btn.configure(corner_radius=5)

cut_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("cut"), "cut.png", padx=10)
cut_btn.configure(corner_radius=5)

paste_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("paste"), "paste.png",
                        padx=10)
paste_btn.configure(corner_radius=5)

rename_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("rename"), "rename.png",
                         padx=10)
rename_btn.configure(corner_radius=5)

delete_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("delete"), "delete.png",
                         padx=10)
delete_btn.configure(corner_radius=5)

new_folder_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2", lambda: print("new folder"),
                             "new_folder.png", padx=10)
new_folder_btn.configure(corner_radius=5)

# # selection pane
selection_pane = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=1, corner_radius=0, height=30)
selection_pane.pack(side=BOTTOM, fill=X)

main_panel = tk.PanedWindow(this_pc.app, bg="white", orient=HORIZONTAL)
main_panel.pack(side=LEFT, fill=BOTH, expand=1)

navigation_pane = tk.PanedWindow(main_panel, width=250)
main_panel.add(navigation_pane)

folder_img = tk.PhotoImage(file="images\\folder_color 20.png")
file_img = tk.PhotoImage(file="images\\file_color_20.png")

middle_pane = tk.PanedWindow(main_panel, bg="white", width=int(this_pc.width - 500))
main_panel.add(middle_pane)

tabletree = ttk.Treeview(middle_pane)
vsb = ttk.Scrollbar(middle_pane, orient="vertical", command=tabletree.yview)

# Create a new style for the vertical scrollbar
# style = ttk.Style()
# style.theme_use('default')  # Ensure the correct theme is used
# style.configure('Vertical.TScrollbar',
#                 width=10,
#                 background='black',
#                 gripcount=0,
#                 arrowsize=0,
#                 borderwidth=10,
#                 troughcolor='black',
#                 relief='flat')
#
# # Apply the new style to the vertical scrollbar
# vsb.configure(style='Vertical.TScrollbar')

vsb.pack(side=RIGHT, fill=Y)
hsb = ttk.Scrollbar(middle_pane, orient="horizontal", command=tabletree.xview)
hsb.pack(side=BOTTOM, fill=X)
tabletree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tabletree.tag_configure("larg", font=("arial", 16))
tabletree["columns"] = ("Name", "File Type", "Size", "Date Created", "Date Modified")

tabletree.column("#0", width=40, minwidth=40, stretch=FALSE)
tabletree.column("Name", width=200, stretch=FALSE)
tabletree.column("File Type", width=100, anchor="center", stretch=FALSE)
tabletree.column("Size", width=100, anchor="center", stretch=FALSE)
tabletree.column("Date Created", width=100, anchor="center", stretch=FALSE)
tabletree.column("Date Modified", width=100, anchor="center", stretch=FALSE)

tabletree.heading("#0", text="", )
tabletree.heading("Name", text="Name", anchor="w")
tabletree.heading("File Type", text="File Type")
tabletree.heading("Size", text="Size")
tabletree.heading("Date Created", text="Date Created")
tabletree.heading("Date Modified", text="Date Modified")

tabletree.pack(side=LEFT, fill=BOTH, expand=1)


def item_select(_):
    print(tabletree.selection())
    for i in tabletree.selection():
        print(tabletree.item(i)["values"][0])
        if tabletree.item(i)["values"][1] == "File":
            print("Files")
        elif tabletree.item(i)["values"][1] == "Folder":
            change_dir(tabletree.item(i)["values"][0])


tabletree.bind("<<TreeviewSelect>>", item_select)

preview_pane = tk.PanedWindow(main_panel, bg="blue", width=250)
main_panel.add(preview_pane)

preview_pane_toggle = TRUE
# toggle preview pane
if preview_pane_toggle:
    main_panel.add(preview_pane)
else:
    main_panel.remove(preview_pane)

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


def enter(frame):
    frame.configure(border_width=2, border_color="lightblue", fg_color="#4c566a")


def exit_(frame):
    frame.configure(fg_color="#434c5e", border_width=0, corner_radius=10)


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
    drive_frame = CTkFrame(navigation_pane, fg_color="#434c5e", border_width=0, corner_radius=10)
    navigation_pane.add(drive_frame)
    drive_frame.grid(row=drives.index(drive), column=0, pady=5, padx=10, sticky="nw")
    # drive_frame.pack(side=LEFT, pady=10, padx=10)

    # drive sizes
    total, used, free = disk_usage(drive[0])
    drives_sizes[drive[0]] = {"total": total, "used": used, "free": free}

    # add an icon for each drive
    png_img = Image.open("images\\hdd_white.PNG")
    png_img = png_img.resize([60, 60])  # Resize the image

    # Convert the image into a CTkImage object
    drive_img = ctk.CTkImage(png_img, size=(35, 35))

    # Create the label with the CTkImage object
    label = ctk.CTkLabel(drive_frame, image=drive_img, text="")
    label.grid(row=0, column=0, rowspan=3, sticky="nw", padx=5, pady=(10, 0))

    # Keep a reference to the image to prevent garbage collection
    label.image = drive_img

    my_font = ctk.CTkFont(family=("Helvetika"), size=14, weight="bold")

    drive_label = CTkLabel(drive_frame, text=drive[1], fg_color="transparent", bg_color="transparent",
                           text_color="white", font=my_font)
    drive_label.grid(row=0, column=1, sticky="nw", pady=(3, 0))

    # Progress bar
    drive_progress_bar = CTkProgressBar(drive_frame, corner_radius=0, border_width=1, height=10,
                                        progress_color="#4681f4")
    drive_progress_bar.set(drives_sizes[drive[0]]["used"] / drives_sizes[drive[0]]["total"])
    drive_progress_bar.grid(row=1, column=1, sticky="nw", padx=(0, 5), pady=0)

    # Drive usage label
    drive_usage = CTkLabel(drive_frame, text=f"{free} GB free of {total} GB", fg_color="transparent",
                           bg_color="transparent", font=("Helvetika", 10))
    drive_usage.grid(row=2, column=1, sticky="nw", pady=(0, 5))

    # Bind left-click event to open the drive
    drive_frame.configure(cursor="hand2")
    print(f"drive before initialization: {drive}")
    drive_frame.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_usage.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))
    drive_progress_bar.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive[0]}"))

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


def open_file(file_path):
    print(f"Opening file: {file_path}")


def open_dir(file_path):
    # this is how th file path looks like: ['C:\\', 'Windows']
    print(f"Opening dir: {file_path}")

    for file in load_files(file_path):
        file_dir = f"{dir_history.get_current_dir()}/{file}"
        if os.path.isfile(file_dir):
            tabletree.insert("", index=tk.END, values=(file, "File", "-", "-", "-"), image=file_img)
        if os.path.isdir(file_dir):
            tabletree.insert("", index=tk.END, values=(file, "Folder", "-", "-", "-"), image=folder_img)


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
