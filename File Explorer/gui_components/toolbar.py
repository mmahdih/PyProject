from tkinter import TOP, LEFT, X, HORIZONTAL, BOTH
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from ttkbootstrap.constants import *

class ToolbarButton(ttk.Button):
    def __init__(self, master, image_path, command, **kwargs):
        # Load the image and resize it
        img = ImageTk.PhotoImage(Image.open(image_path).resize((25, 25)))
        super().__init__(master, image=img, command=command, **kwargs)
        self.image = img  # Prevent garbage collection of the image object


# Function to create the toolbar
def create_toolbar(app, commands):
    toolbar = ttk.Frame(app, height=30)
    toolbar.pack(side=TOP, fill=X, ipady=10, ipadx=10)

    for (image_path, command) in commands:
        btn = ToolbarButton(toolbar, image_path, command, style="Outline.TButton")
        btn.pack(side=LEFT, padx=10)

    return toolbar


# Function to create the selection pane
def create_selection_pane(app):
    selection_pane = ctk.CTkFrame(app, fg_color="#E8E8E8", border_width=1, corner_radius=0, height=30)
    selection_pane.pack(side=BOTTOM, fill=X)
    return selection_pane


# Function to create the main panel
def create_main_panel(app):
    main_panel = ttk.PanedWindow(app, orient=HORIZONTAL)
    main_panel.pack(side=LEFT, fill=BOTH, expand=1)
    return main_panel

def create_navigation_pane(main_panel):
    navigation_pane = ttk.PanedWindow(main_panel, width=250)
    main_panel.add(navigation_pane)
    return navigation_pane

def create_middle_pane(main_panel):
    middle_pane = ttk.PanedWindow(main_panel, width=1000, orient=VERTICAL)
    main_panel.add(middle_pane)

    return middle_pane

def create_preview_pane(main_panel):
    preview_pane = ttk.PanedWindow(main_panel, width=250)
    main_panel.add(preview_pane)

    return preview_pane