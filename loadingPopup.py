import tkinter as tk
from tkinter import ttk

class LoadingPopup:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.popup = None

    def show(self):
        self.root.config(cursor='exchange')
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Loading")
        ttk.Label(self.popup, image=self.config['clock']).pack()

        self.popup.update_idletasks()
        width = self.popup.winfo_width()
        height = self.popup.winfo_height()

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        self.popup.geometry(f"300x300+{x}+{y}")
        self.popup.grab_set()
        self.popup.update()

    def close(self):
        if self.popup:
            self.root.config(cursor='')
            self.popup.destroy()