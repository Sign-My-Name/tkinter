import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proj_camera import proj_camera
from proj_logger import get_logger


# main identify Frame
class IdentifyPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info(f'IdentifyPage init...')
        self.config = config
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.middle_frame_identify = MiddleIdentifyFrame(self, self.config)
        self.top_frame_identify = BottomIdentifyFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        self.config["cap"].close_camera()
        self.pack_forget()


# middle main frame
class MiddleIdentifyFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='top', expand=True, fill='both', pady=15)
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        self.middle_left = MiddleLeftIdentifyFrame(self, self.config)
        self.middle_right = MiddleRightIdentifyFrame(self, self.config)


# middle left frame
class MiddleLeftIdentifyFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='left', fill='both', expand=True)
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        identify_boy_label = tk.Label(self, image=self.config["boy_img"], bg=self.config["BG_COLOR"])
        identify_boy_label.pack(side='bottom',padx=10, expand=True)


# middle right frame
class MiddleRightIdentifyFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(expand=True, fill='both')
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        # prediction frame
        self.prediction_frame = tk.Frame(self, bg=self.config["BG_COLOR"], padx=10, pady=5)
        self.prediction_frame.pack(side="top", pady=0, padx=20, fill='x') 

        self.empty_frame1 = tk.Label(self.prediction_frame, width=int(self.prediction_frame.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='left', expand=True, fill='x')

        # prediction label
        self.prediction_label = tk.Label(self.prediction_frame, text="", bg=self.config["BG_COLOR"],
                                         font=("Calibre", 80, 'bold')) 
        self.prediction_label.pack(side="left", pady=0)

        self.empty_frame2 = tk.Label(self.prediction_frame, width=int(self.prediction_frame.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='left', expand=True, fill='x')

        # prediction header
        self.prediction_label_header = tk.Label(self.prediction_frame, image=self.config["meet_the_letter"],
                                                bg=self.config["BG_COLOR"]) 
        self.prediction_label_header.pack(side='left', pady=3, padx=15)

        self.empty_frame3 = tk.Label(self.prediction_frame, width=int(self.prediction_frame.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame3.pack(side='left', expand=True, fill='x')

        # video frame
        self.identify_video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.identify_video_label.pack(side='top', fill='both',padx=30, expand=True)

        # starting camera
        self.config["cap"].start_camera(self.identify_video_label, self.prediction_label)


# Bottom frame
class BottomIdentifyFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.pack(side='top', fill='x')
        self.create_widgets()

    def back_to_homepage(self):
        self.parent.close_frame()
        self.config["homePage_show"]()

    def create_widgets(self):
        back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0, command=self.back_to_homepage, activebackground=self.config["BG_COLOR"])
        back_button.pack(side='right', padx=30, pady=10)
