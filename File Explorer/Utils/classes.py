

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

