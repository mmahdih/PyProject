import ttkbootstrap as ttk

root = ttk.Window()
root.title("My Application")

tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

tab1 = ttk.Frame(tab_control, width=200, height=200)
tab_control.add(tab1, text="Tab 1")

tab2 = ttk.Frame(tab_control, width=200, height=200)
tab_control.add(tab2, text="Tab 2")

def add_new_tab(tab_name):
    tab = ttk.Frame(tab_control, width=200, height=200)
    tab_control.add(tab, text=f"{tab_name}")


add_new_tab("Tab 3")
add_new_tab("Tab 4")
add_new_tab("Tab 5")
add_new_tab("Tab 6")

root.mainloop()