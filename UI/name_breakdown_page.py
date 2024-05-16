import tkinter as tk
from proj_camera import proj_camera
from proj_logger import get_logger

# Main NameBreakdown Frame
class NameBreakdownPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info('Initializing NameBreakdownPage...')
        self.config = config
        self.top_frame = TopFrame(self, self.config)
        self.middle_frame = MiddleFrame(self, self.config)
        self.bottom_frame = BottomFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        self.pack_forget()

# Top Frame
class TopFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.pack(side='top', fill='x')
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="What's your name?", font=("Calibri", 20), bg=self.config["BG_COLOR"])
        self.name_label.pack(side="top", padx=10)

        self.entry = tk.Entry(self, font=("Calibri", 20), justify="right")
        self.entry.pack(side="left", padx=10)

        self.submit_button = tk.Button(self, image=self.config["submit_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                       command=self.submit_name,
                                       highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                       highlightthickness=0)
        self.submit_button.pack(side="left", padx=10)

        self.back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                     command=self.back_to_homepage,
                                     highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                     highlightthickness=0)
        self.back_button.pack(side="right", padx=10)

    def submit_name(self):
        name = self.entry.get()
        self.parent.middle_frame.display_name(name)

    def back_to_homepage(self):
        self.parent.close_frame()
        self.config["homePage_show"]()

# Middle Frame
class MiddleFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side='top', expand=True, fill='both')
        self.letter_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.letter_label.pack(side="left", padx=10)

        self.next_button = tk.Button(self, image=self.config["next_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                     command=self.display_next_letter,
                                     highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                     highlightthickness=0)
        self.next_button.pack_forget()

    def display_name(self, name):
        self.name_letters = list(name)
        self.current_letter_index = 0
        if self.name_letters:
            self.display_letter(self.name_letters[0])

    def display_letter(self, letter):
        self.letter_label.config(text=letter)

    def display_next_letter(self):
        self.current_letter_index += 1
        if self.current_letter_index < len(self.name_letters):
            self.display_letter(self.name_letters[self.current_letter_index])
        else:
            self.next_button.pack_forget()

# Bottom Frame
class BottomFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side='bottom', fill='x')
        self.congrats_label = tk.Label(self, text="", bg=self.config["BG_COLOR"], font=("Arial", 20))
        self.congrats_label.pack(side="bottom", pady=10)

    def display_congrats(self, message):
        self.congrats_label.config(text=message)
