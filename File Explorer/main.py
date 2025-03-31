import os
import string
from ctypes import windll
from shutil import disk_usage
from tkinter import *
from typing import Union, Callable

import customtkinter as ctk
import cv2
import psutil
from PIL import Image
from customtkinter import *


# import numpy as np

# ctk.deactivate_automatic_dpi_awareness()

# custom scaling
# ctk.set_window_scaling(0.8)
# ctk.set_widget_scaling(0.8)

# the Main window
class Window:
	def __init__(self, width, height, app):
		self.width = width
		self.height = height
		self.app = app
		self.app.title("File Explorer")
		self.app.geometry(f"{self.width}x{self.height}")
		self.app.attributes("-topmost", True)

	def fullscreen_toggle(self):
		self.app.attributes("-fullscreen", not self.app.attributes("-fullscreen"))


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
dir_history = DirectoryHistory()

# make the main window
this_pc = Window(600, 600, CTk())

# bind the F11 key to toggle fullscreen
this_pc.app.bind("<F11>", lambda event: this_pc.fullscreen_toggle())
if this_pc.app.state() != "normal":
	this_pc.app.bind("<Escape>", lambda event: this_pc.fullscreen_toggle())
print("state: ", this_pc.app.state())


# this_pc.app.bind("<F1>", lambda event: bigger_screen())

def open_foto(name):
	this_pc.app.geometry("1500x600")
	global image_frame
	image_frame = ctk.CTkFrame(this_pc.app, width=700, height=394)
	image_frame.grid(row=0, column=3, rowspan=10, sticky="nsew", pady=10, padx=10)

	image_dir = f"{dir_history.get_current_dir()}\\{name}"
	print(image_dir)

	# my_image = Image.open("images\\hdd_white.PNG")
	# my_image = my_image.resize([60, 60])  # Resize the image
	#
	# # Convert the image into a CTkImage object
	# drive_img = ctk.CTkImage(png_img, size=(60, 60))
	#
	# # Create the label with the CTkImage object
	# label = ctk.CTkLabel(drive_frame, image=drive_img, text="")
	# label.grid(row=0, column=0, rowspan=3, sticky="nw", padx=5, pady=(10, 0))
	#
	# # Keep a reference to the image to prevent garbage collection
	# label.image = drive_img

	my_image = Image.open(image_dir)
	width, height = my_image.size
	scale = min(700 / width, 394 / height)
	new_width = int(width * scale)
	new_height = int(height * scale)
	# my_image = my_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
	# Resize the image to fit the frame while keeping the aspect ratio
	# print(f"iamge width: {width}, hight: {height}")
	# print(f"iamge width: {new_width}, hight: {new_height}")
	# my_image = my_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
	the_image = ctk.CTkImage(my_image, size=(new_width, new_height))

	# Calculate the x and y offset to center the image
	x_offset = (550 - new_width) // 2
	y_offset = (550 - new_height) // 2

	# Create the label with the CTkImage object
	label = ctk.CTkLabel(image_frame, image=the_image, text="")
	label.place(relx=0.5, rely=0.5, anchor="center")
	# Keep a reference to the image to prevent garbage collection
	label.image = my_image


def open_new_window(name):
	image_dir = f"{dir_history.get_current_dir()}\\{name}"

	im = cv2.imread(image_dir)
	height, width, _ = im.shape
	scale = min(700 / width, 394 / height)
	cv2.namedWindow("image", cv2.WINDOW_NORMAL)
	cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	new_width = int(width * scale)
	new_height = int(height * scale)
	# im = cv2.resize(im, (new_width, new_height))
	cv2.imshow("image", im)
	cv2.waitKey()


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
	drive_label.grid(row=0, column=1, sticky="nw", pady=(2, 5))

	# Progress bar
	drive_progress_bar = CTkProgressBar(drive_frame, height=18, corner_radius=0)
	drive_progress_bar.set(drives_sizes[drive]["used"] / drives_sizes[drive]["total"])
	drive_progress_bar.grid(row=1, column=1, sticky="nw", padx=(0, 10))

	# Drive usage label
	drive_usage = CTkLabel(drive_frame, text=f"{free} GB free of {total} GB")
	drive_usage.grid(row=2, column=1, pady=(5, 2), sticky="nw")

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
dir_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
dir_frame.grid_columnconfigure(0, weight=0)
dir_frame.grid_columnconfigure(0, weight=1)


def switch_event():
	print("switch toggled, current value:", switch_var.get())
	if switch_var.get() == "on":
		ctk.set_appearance_mode("dark")
	else:
		ctk.set_appearance_mode("light")


switch_var = ctk.StringVar(value="on")
switch = ctk.CTkSwitch(this_pc.app, text="Dark Mode", command=switch_event,
                       variable=switch_var, onvalue="on", offvalue="off")
switch.grid(row=5, column=0, columnspan=2, padx=10, sticky="w")

# Initialize appearance mode based on the initial value of switch_var
switch_event()

if __name__ == "__main__":
	this_pc.app.mainloop()
