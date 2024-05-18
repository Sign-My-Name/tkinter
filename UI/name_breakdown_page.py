import tkinter as tk
import os
from PIL import Image, ImageTk, ImageOps
from proj_camera import proj_camera
from proj_logger import get_logger

# Main NameBreakdown Frame
class NameBreakdownPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info('Initializing NameBreakdownPage...')
        self.config = config
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.top_frame = TopFrame(self, self.config)
        self.middle_frame = MiddleFrame(self, self.config)
        self.bottom_frame = BottomFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        self.config["cap"].close_camera()
        self.pack_forget()

# Top Frame
class TopFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.config["back_to_homepage"] = self.back_to_homepage
        self.what_your_name = config["whats_your_name_img"]
        self.name = None
        self.pack(side='top', fill='x')
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self, image=self.what_your_name, font=("Calibri", 20), bg=self.config["BG_COLOR"])
        self.name_label.pack(side="top", padx=10)

        self.empty_frame1 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='left', expand=True)

        self.submit_button = tk.Button(self, image=self.config["submit_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                       command=self.submit_name,
                                       highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                       highlightthickness=0)
        self.submit_button.pack(side="left", padx=10)


        self.entry = tk.Entry(self, font=("Calibri", 20), justify="right")
        self.entry.pack(side="left", padx=10)


        self.empty_frame3 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame3.pack(side='left', expand=True)


    def submit_name(self):
        self.name = self.entry.get()
        self.parent.middle_frame.middle_left_frame.display_name(self.name)

    def back_to_homepage(self):
        self.parent.close_frame()
        self.config["homePage_show"]()



class MiddleFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.middle_left_frame = MiddleLeftFrame(self, self.config)
        self.empty_frame = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame.pack(side='right', expand=True)
        self.middle_right_frame = MiddleRightFrame(self, self.config)
        self.pack(expand=True, fill="both")


class MiddleRightFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"]) 
        self.config = config
        self.pack(side='right')
        self.create_widgets()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, height=int(self.winfo_height() / 2),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)

        self.empty_frame2 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='left', expand=True)
        self.name_breakdown_video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.name_breakdown_video_label.pack(side='left', fill='both', expand=True)
        self.prediction_label = tk.Label(self, text="", bg=self.config["BG_COLOR"],
                                         font=("Calibre", 80, 'bold'))
        # self.prediction_label.pack()
        self.config["cap"].start_camera(self.name_breakdown_video_label, self.prediction_label)

# Middle Left Frame
class MiddleLeftFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"]) 
        self.config = config
        self.name = None
        self.pack(side='left', expand=True, fill='both')
        self.empty = ImageTk.PhotoImage(Image.open("letters/empty.png").resize((300, 300), Image.LANCZOS))
        self.letter_label = tk.Label(self,image=self.empty, bg=self.config["BG_COLOR"])
        self.letter_label.pack(side="right")
        self.next_button = tk.Button(self, image=self.config["next_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                     command=self.display_next_letter,
                                     highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                     highlightthickness=0)
        self.next_button.pack_forget()

    def display_name(self, name):
        self.name = name
        self.name_letters = list(name)
        self.current_letter_index = 0
        if self.name_letters:
            self.display_letter(self.name_letters[0])

    def display_letter(self, letter):
        image_file = f"letters/{letter}.png"
        if os.path.exists(image_file):
            image = Image.open(image_file)
            image = ImageOps.exif_transpose(image)  # Rotate the image based on EXIF metadata
            image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
            self.letter_label.config(image=image, fg="black")  # Reset the foreground color
            self.letter_label.image = image  # Keep a reference to prevent garbage collection
        else:
            self.letter_label.config(text=letter, image="", font=("Calibri", 34))

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
        self.flag = 0
        self.congrats = self.config["congrats"]
        self.pack(side='bottom', fill='x')
        self.congrats_label = tk.Label(self, text="", bg=self.config["BG_COLOR"], font=("Arial", 20))
        self.congrats_label.pack(side="left", pady=10)
        # self.display_congrats()
        self.create_widgets()
    def return_to_homepage(self):
        self.config["back_to_homepage"]()

    def create_widgets(self):
        self.back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                     command=self.return_to_homepage,
                                     highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                     highlightthickness=1)
        self.back_button.pack(side="right", padx=10)
    def display_congrats(self):
        if self.flag == 0:
            self.congrats_label.config(image=self.congrats)
            self.flag = 1
        else:
            self.congrats_label.config(image="")
            self.flag = 0
