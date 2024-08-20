import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proj_camera import proj_camera
from proj_logger import get_logger


# main identify Frame
class WordIdentifyPage(tk.Frame):
    """
    Main frame for the Word Identify Page, responsible for initializing camera and UI components.
    """
    def __init__(self, parent, config):
        """
        Initializes the WordIdentifyPage with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info(f'WordIdentify init...')
        self.config = config
        self.cap = proj_camera()
        self.cap.set_confidence(0.7)
        self.config["cap"] = self.cap
        self.middle_frame_identify = MiddleWordIdentifyFrame(self, self.config)
        self.top_frame_identify = BottomWordIdentifyFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        """
        Closes the WordIdentifyPage and stops the camera.
        """
        self.config["cap"].close_camera()
        self.pack_forget()


# middle main frame
class MiddleWordIdentifyFrame(tk.Frame):
    """
    Middle frame of the Word Identify Page, containing the main interactive elements.
    """
    def __init__(self, parent, config):
        """
        Initializes the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='top', expand=True, fill='both', pady=15)
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the middle frame.
        """
        self.middle_left = MiddleWordLeftIdentifyFrame(self, self.config)
        self.middle_right = MiddleWordRightIdentifyFrame(self, self.config)


# middle left frame
class MiddleWordLeftIdentifyFrame(tk.Frame):
    """
    Left section of the middle frame, displaying the identification character and spacing.
    """
    def __init__(self, parent, config):
        """
        Initializes the left section of the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='left', fill='both', expand=True)
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the left section of the middle frame.
        """
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        identify_boy_label = tk.Label(self, image=self.config["boy_img"], bg=self.config["BG_COLOR"])
        identify_boy_label.pack(side='bottom', padx=10, expand=True)


# middle right frame
class MiddleWordRightIdentifyFrame(tk.Frame):
    """
    Right section of the middle frame, containing the prediction label and video feed.
    """
    def __init__(self, parent, config):
        """
        Initializes the right section of the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(expand=True, fill='both')
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the right section of the middle frame.
        """
        # prediction frame
        self.middle_top_frame = tk.Frame(self, bg=self.config["BG_COLOR"])
        self.middle_top_frame.pack(side="top",expand=True, fill='both') 

        self.empty_frame1 = tk.Label(self.middle_top_frame, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='left', expand=True, fill='x')

        # prediction label
        self.prediction_label = tk.Label(self.middle_top_frame, text="", bg=self.config["BG_COLOR"],
                                         font=("Guttman Yad-Brush", 80, 'bold')) 
        self.prediction_label.pack(side="left", pady=0)

        self.empty_frame2 = tk.Label(self.middle_top_frame, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='left', expand=True, fill='x')

        # prediction header
        self.prediction_label_header = tk.Label(self.middle_top_frame, image=self.config["meet_the_word"],
                                                bg=self.config["BG_COLOR"]) 
        self.prediction_label_header.pack(side='left', pady=0, padx=2)

        self.empty_frame3 = tk.Label(self.middle_top_frame, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame3.pack(side='left', expand=True, fill='x')

        # video frame
        self.identify_video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.identify_video_label.pack(side='top', fill='both',padx=30, expand=True)

        # starting camera
        self.config["cap"].start_camera(self.identify_video_label, self.prediction_label, "words")


# bottom frame
class BottomWordIdentifyFrame(tk.Frame):
    """
    Bottom frame of the Word Identify Page, containing navigation controls.
    """
    def __init__(self, parent, config):
        """
        Initializes the bottom frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.pack(side='top', fill='both', expand=True)
        self.create_widgets()

    def back_to_homepage(self):
        """
        Returns to the HomePage.
        """
        self.parent.close_frame()
        self.config["homePage_show"]()

    def create_widgets(self):
        """
        Creates widgets in the bottom frame.
        """
        back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0, command=self.back_to_homepage, highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                highlightthickness=0, activebackground=self.config["BG_COLOR"], cursor="hand2")
        back_button.pack(side='right', padx=30, pady=10)
