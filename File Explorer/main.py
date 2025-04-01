import os
import string
from ctypes import windll
from datetime import datetime
from shutil import disk_usage
from tkinter import *
from tkinter import ttk
from typing import Union, Callable

import customtkinter as ctk
import cv2
import psutil
from PIL import Image
from customtkinter import *
import numpy as np















# ctk.deactivate_automatic_dpi_awareness()

# custom scaling
# ctk.set_window_scaling(0.8)
# ctk.set_widget_scaling(0.8)


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
this_pc = Window(1500, 800, CTk())


class Make_Button(ctk.CTkButton):
	def __init__(self, parent, text, width, height, fg_color, hover_color, cursor, command, image=None, padx=0, pady=0):
		super().__init__(parent, text=text, command=command, width=width, height=height, fg_color=fg_color, hover_color=hover_color, cursor=cursor, compound="left", border_width=0)

		if image is not None:
			image = "images\\" + image
			image = ctk.CTkImage(Image.open(image), size=(width, height))
			self.configure(image=image, compound="left")

		self.pack(side=LEFT, padx=padx, pady=pady)

	def img(self, image, width, height):
		image = "images\\" + image
		image = ctk.CTkImage(Image.open(image), size=(width, height))
		self.configure(image=image, compound="left")


	# def bind(self, button, command, event=None):
	# 	super().bind( f"<{button}>", lambda: command(event) )


toolbar = ctk.CTkFrame(this_pc.app, fg_color="lightblue", border_width=1, corner_radius=0, height=40)
toolbar.pack(side=TOP, fill=X, ipady=10, ipadx=10)

back_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("back"), "back.png", padx=(10, 1))
back_btn.configure(corner_radius=5)
# back_btn.bind("<Enter>", lambda event: back_btn.img("white\\back.png", 20, 20))
# back_btn.bind("<Leave>", lambda event: back_btn.img("back.png", 20, 20))


forward_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("forward"), "forward.png")
forward_btn.configure(corner_radius=5)
# forward_btn.bind("<Enter>", lambda event: forward_btn.configure(hover_color="#4c566a") and forward_btn.img("white\\forward.png", 20, 20))
# forward_btn.bind("<Leave>", lambda event: forward_btn.img("forward.png", 20, 20))

# preview pane toolbar button
preview_pane_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("preview pane"), "preview_pane.png", padx=10)
preview_pane_btn.configure(corner_radius=5)

copy_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("copy"), "copy.png", padx=10)
copy_btn.configure(corner_radius=5)

cut_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("cut"), "cut.png", padx=10)
cut_btn.configure(corner_radius=5)

paste_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("paste"), "paste.png", padx=10)
paste_btn.configure(corner_radius=5)

rename_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("rename"), "rename.png", padx=10)
rename_btn.configure(corner_radius=5)

delete_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("delete"), "delete.png", padx=10)
delete_btn.configure(corner_radius=5)

new_folder_btn = Make_Button(toolbar, "", 20, 20, "#eceff4", "#4681f4", "hand2",  lambda: print("new folder"), "new_folder.png", padx=10)
new_folder_btn.configure(corner_radius=5)




# selection pane
selection_pane = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=1, corner_radius=0, height=40)
selection_pane.pack(side=BOTTOM, fill=X)

# preview pane
navigation_pane = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=1, corner_radius=0, width=int(this_pc.width * 0.20))
navigation_pane.pack(side=LEFT, fill=Y)



# folders view part
display = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=1, corner_radius=0, width=int(this_pc.width * 0.60))
display.pack(side=LEFT, fill=BOTH, expand=True)


# make a table for folders
folder_tree = ttk.Treeview(this_pc.app)
folder_tree["columns"] = ("Name", "File Type", "Size", "Date Created", "Date Modified")

folder_tree.heading("#0", text="Path")
folder_tree.heading("Name", text="Name")
folder_tree.heading("File Type", text="File Type")
folder_tree.heading("Size", text="Size")
folder_tree.heading("Date Created", text="Date Created")
folder_tree.heading("Date Modified", text="Date Modified")

folder_tree.column("#0", width=150)
folder_tree.column("Name", anchor="center", width=100)
folder_tree.column("File Type", anchor="center", width=100)
folder_tree.column("Size", anchor="center", width=100)
folder_tree.column("Date Created", anchor="center", width=150)
folder_tree.column("Date Modified", anchor="center", width=150)

folder_tree.insert("", "end", "C:\\", text="C:\\", values=("Folder", "-", "-", "-", "-"))
folder_tree.insert("", "end", "D:\\", text="D:\\", values=("Folder", "-", "-", "-", "-"))




# preview pane
preview_pane = ctk.CTkFrame(this_pc.app, fg_color="#E8E8E8", border_width=0, corner_radius=0, width=int(this_pc.width * 0.20))
preview_pane.pack(side=RIGHT, fill=BOTH, expand=True)

# preview pane toolbar img
img1 = Image.open("images\\pexels-francesco-ungaro-2325447.jpg")
# width, height = img1.size
new_width = int(100 * (16 / 9))
ttk_img1 = ctk.CTkImage(img1.resize((new_width, 100)), size=(new_width, 100))
img_label = ctk.CTkLabel(preview_pane, text="", image=ttk_img1)
img_label.pack(side=TOP, pady=(60,0))

file_label = ctk.CTkLabel(preview_pane, text="Image 1.jpg", font=ctk.CTkFont(family=("Helvetika"), size=20, weight="normal"), fg_color="#E8E8E8", text_color="black")
file_label.pack(side=TOP, fill=X, pady=(10, 0))

date_created = ctk.CTkLabel(preview_pane, text=f"Date Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" , font=ctk.CTkFont(family=("Helvetika"), size=12, weight="normal"), fg_color="#E8E8E8", text_color="black")
date_created.pack(side=TOP, fill=X, pady=(10, 0))

date_modified = ctk.CTkLabel(preview_pane, text=f"Date Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", font=ctk.CTkFont(family=("Helvetika"), size=12, weight="normal"), fg_color="#E8E8E8", text_color="black")
date_modified.pack(side=TOP, fill=X, pady=(10, 0))









# this_pc.app.columnconfigure(0, weight=1)
# this_pc.app.columnconfigure(0, weight=2)
# this_pc.app.columnconfigure(1, weight=1)
# # split the main window into parts
# # assign the first row for toolbar


#
# # fill the columns with color
# label = ctk.CTkLabel(this_pc.app, text="Hello", fg_color="blue", text_color=("gray10", "gray90"))
# label.grid(row=0, column=0, sticky="nsew", padx=5, pady=(10, 0), columnspan=3)
#
#
# label1 = ctk.CTkLabel(this_pc.app, text="Hello", fg_color="transparent", text_color=("gray10", "gray90"))
# label1.grid(row=0, column=1, sticky="nsew", padx=5, pady=(10, 0))
#
# label2 = ctk.CTkLabel(this_pc.app, text="Hello", fg_color="transparent", text_color=("gray10", "gray90"))
# label2.grid(row=0, column=2, sticky="nsew", padx=5, pady=(10, 0))


class FloatSpinbox(ctk.CTkFrame):
	def __init__(self, *args,
	             width: int = 100,
	             height: int = 32,
	             step_size: Union[int, float] = 1,
	             command: Callable = None,
	             **kwargs):
		super().__init__(*args, width=width, height=height, **kwargs)

		self.step_size = step_size
		self.command = command

		self.configure(fg_color=("gray78", "gray28"))  # set frame color

		self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
		self.grid_columnconfigure(1, weight=1)  # entry expands

		self.subtract_button = ctk.CTkButton(self, text="-", width=height - 6, height=height - 6,
		                                     command=self.subtract_button_callback)
		self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

		self.entry = ctk.CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
		self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

		self.add_button = ctk.CTkButton(self, text="+", width=height - 6, height=height - 6,
		                                command=self.add_button_callback)
		self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

		# default value
		self.entry.insert(0, "0.0")

	def add_button_callback(self):
		if self.command is not None:
			self.command()
		try:
			value = float(self.entry.get()) + self.step_size
			self.entry.delete(0, "end")
			self.entry.insert(0, value)
		except ValueError:
			return

	def subtract_button_callback(self):
		if self.command is not None:
			self.command()
		try:
			value = float(self.entry.get()) - self.step_size
			self.entry.delete(0, "end")
			self.entry.insert(0, value)
		except ValueError:
			return

	def get(self) -> Union[float, None]:
		try:
			return float(self.entry.get())
		except ValueError:
			return None

	def set(self, value: float):
		self.entry.delete(0, "end")
		self.entry.insert(0, str(float(value)))

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



# # bind the F11 key to toggle fullscreen
# this_pc.app.bind("<F11>", lambda event: this_pc.fullscreen_toggle())
# if this_pc.app.state() != "normal":
# 	this_pc.app.bind("<Escape>", lambda event: this_pc.fullscreen_toggle())
# print("state: ", this_pc.app.state())
#
#
# # this_pc.app.bind("<F1>", lambda event: bigger_screen())
#
# def open_foto(name):
# 	this_pc.app.geometry("1500x600")
# 	global image_frame
# 	image_frame = ctk.CTkFrame(this_pc.app, width=700, height=394)
# 	image_frame.grid(row=0, column=3, rowspan=10, sticky="nsew", pady=10, padx=10)
#
# 	image_dir = f"{dir_history.get_current_dir()}\\{name}"
# 	print(image_dir)
#
# 	# my_image = Image.open("images\\hdd_white.PNG")
# 	# my_image = my_image.resize([60, 60])  # Resize the image
# 	#
# 	# # Convert the image into a CTkImage object
# 	# drive_img = ctk.CTkImage(png_img, size=(60, 60))
# 	#
# 	# # Create the label with the CTkImage object
# 	# label = ctk.CTkLabel(drive_frame, image=drive_img, text="")
# 	# label.grid(row=0, column=0, rowspan=3, sticky="nw", padx=5, pady=(10, 0))
# 	#
# 	# # Keep a reference to the image to prevent garbage collection
# 	# label.image = drive_img
#
# 	my_image = Image.open(image_dir)
# 	width, height = my_image.size
# 	scale = min(700 / width, 394 / height)
# 	new_width = int(width * scale)
# 	new_height = int(height * scale)
# 	# my_image = my_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
# 	# Resize the image to fit the frame while keeping the aspect ratio
# 	# print(f"iamge width: {width}, hight: {height}")
# 	# print(f"iamge width: {new_width}, hight: {new_height}")
# 	# my_image = my_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
# 	the_image = ctk.CTkImage(my_image, size=(new_width, new_height))
#
# 	# Calculate the x and y offset to center the image
# 	x_offset = (550 - new_width) // 2
# 	y_offset = (550 - new_height) // 2
#
# 	# Create the label with the CTkImage object
# 	label = ctk.CTkLabel(image_frame, image=the_image, text="")
# 	label.place(relx=0.5, rely=0.5, anchor="center")
# 	# Keep a reference to the image to prevent garbage collection
# 	label.image = my_image
#
#
# def open_new_window(name):
# 	image_dir = f"{dir_history.get_current_dir()}\\{name}"
#
# 	im = cv2.imread(image_dir)
# 	height, width, _ = im.shape
# 	scale = min(700 / width, 394 / height)
# 	cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# 	cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# 	new_width = int(width * scale)
# 	new_height = int(height * scale)
# 	# im = cv2.resize(im, (new_width, new_height))
# 	cv2.imshow("image", im)
# 	cv2.waitKey()
#
#
def enter(frame):
	# print("Entered the frame")
	frame.configure(border_width=2, border_color="lightblue", fg_color="#4c566a")


def exit_(frame):
	# print("Exited the frame")
	frame.configure(fg_color="#434c5e", border_width=0, corner_radius=10)


def initial_dir(dir_name):
	dir_history.clear_history()
	dir_history.set_initial_dir(dir_name)
	print("Initial Directory:", dir_name)
	open_dir(dir_name)


def change_dir(dir_name):
	print("Current Directory: B: ", dir_history.get_current_dir())
	new_dir = dir_history.change_dir(dir_name)
	print("Current Directory: A: ", dir_history.get_current_dir())
	open_dir(new_dir)


def back():
	print("Current Directory: B: ", dir_history.get_current_dir())
	new_dir = dir_history.go_back()
	print("Current Directory: A: ", dir_history.get_current_dir())
	open_dir(new_dir)


def make_drive_frames(drive):
	drive_frame = CTkFrame(navigation_pane, fg_color="#434c5e", border_width=0, corner_radius=10)
	drive_frame.grid(row=drives.index(drive), column=0, pady=5, padx=10, sticky="nw")
	# drive_frame.pack(side=LEFT, pady=10, padx=10)

	# drive sizes
	total, used, free = disk_usage(drive)
	drives_sizes[drive] = {"total": total, "used": used, "free": free}

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

	# Drive label
	name = ""
	if (drive == "C"):
		name = f"{drive}: Windows"
	elif (drive == "D"):
		name = f"{drive}: Personal Files"

	drive_label = CTkLabel(drive_frame, text=name, font=my_font)
	drive_label.grid(row=0, column=1, sticky="nw", pady=(3,0))

	# Progress bar
	drive_progress_bar = CTkProgressBar(drive_frame, corner_radius=0, border_width=1)
	drive_progress_bar.set(drives_sizes[drive]["used"] / drives_sizes[drive]["total"])
	drive_progress_bar.grid(row=1, column=1, sticky="nw", padx=(0,5), pady=0)

	# Drive usage label
	drive_usage = CTkLabel(drive_frame, text=f"{free} GB free of {total} GB", fg_color="transparent", bg_color="transparent", font=("Helvetika", 10))
	drive_usage.grid(row=2, column=1, sticky="nw", pady=0)

	# Bind left-click event to open the drive
	drive_frame.configure(cursor="hand2")
	drive_frame.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive}:"))
	label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive}:"))
	drive_label.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive}:"))
	drive_usage.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive}:"))
	drive_progress_bar.bind("<Button-1>", lambda d=drive: initial_dir(f"{drive}:"))

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

#
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
	used = round(hdd.used / 1024 / 1024 / 1024, 2)
	free = round(hdd.free / 1024 / 1024 / 1024, 2)

	print(f"DISK Total: {total} GB")
	print(f"Disk Used: {used} GB")
	print(f"Disk Free: {free} GB")

	return total, used, free


def make_buttons(frame, name, type):
	if (type == "file"):
		button = ""
		button = CTkButton(frame, text=name, font=ctk.CTkFont(family=("Helvetika"), size=20, weight="bold"),
		                   fg_color="#434c5e", hover_color="#4c566a", cursor="hand2", command=lambda: open_foto(name))
		button.bind("<Double-Button-1>", lambda event: open_new_window(name))
		button.pack(pady=10)
	elif (type == "folder"):
		button = ""
		button = CTkButton(frame, text=name, font=ctk.CTkFont(family=("Helvetika"), size=20, weight="bold"),
		                   fg_color="#434c5e", hover_color="#4c566a", cursor="hand2", command=lambda: change_dir(name))
		button.pack(pady=10)


# button.bind("<Button-3>", lambda d=name: run_app(f"{dir_history.get_current_dir()}/{name}"))


def clear_all_inside_frame(frame):
	# Iterate through every widget inside the frame

	for widget in frame.winfo_children():
		widget.destroy()  # deleting widget


def open_file(file_path):
	print(f"Opening file: {file_path}")


def open_dir(file_path):
	print(f"Opening file: {file_path}")

	clear_all_inside_frame(dir_frame)

	if dir_history.get_current_dir() not in ["C:", "D:"]:
		button = CTkButton(dir_frame, text="Back", font=ctk.CTkFont(family=("Helvetika"), size=20, weight="bold"),
		                   fg_color="#d08770", hover_color="#d08780", cursor="hand2", command=lambda: back())
		button.pack(pady=10)
	for file in load_files(file_path):
		file_dir = f"{dir_history.get_current_dir()}/{file}"
		# print(f"files: {file_dir}")
		if os.path.isfile(file_dir):
			make_buttons(dir_frame, file, "file")
		# print("IT is a file.")
		if os.path.isdir(file_dir):
			make_buttons(dir_frame, file, "folder")
		# print("IT is a folder.")


def load_files(file_path):
	files = os.listdir(f"{file_path}\\")
	return files


drives_sizes = {}

# make a frame for every drive in this pc
for drive in drives:
	# Create the parent frame for the drive
	make_drive_frames(drive)

dir_frame = ctk.CTkScrollableFrame(this_pc.app, label_text="Files", height=380)
# dir_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
# dir_frame.grid_columnconfigure(0, weight=0)
# dir_frame.grid_columnconfigure(0, weight=1)


def switch_event():
	print("switch toggled, current value:", switch_var.get())
	if switch_var.get() == "on":
		ctk.set_appearance_mode("dark")
	else:
		ctk.set_appearance_mode("light")


switch_var = ctk.StringVar(value="on")
switch = ctk.CTkSwitch(this_pc.app, text="Dark Mode", command=switch_event,
                       variable=switch_var, onvalue="on", offvalue="off")
# switch.grid(row=5, column=0, columnspan=2, padx=10, sticky="w")

# Initialize appearance mode based on the initial value of switch_var
switch_event()

if __name__ == "__main__":
	this_pc.app.mainloop()
