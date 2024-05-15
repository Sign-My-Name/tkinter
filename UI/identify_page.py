import tkinter as tk
import sys
import os
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proj_camera import proj_camera
from proj_logger import get_logger



# main identify Frame
class IdentifyPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info(f'starting init of IdentifyPage')
        self.config = config
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.top_frame_identify = TopIdentifyFrame(self, self.config)
        self.middle_frame_identify = MiddleIdentifyFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        
        self.config["cap"].close_camera()
        self.pack_forget()

# top frame
class TopIdentifyFrame(tk.Frame):
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
        back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0, command= self.back_to_homepage,
                                highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"], highlightthickness=0)
        back_button.pack(side='right', padx=30, pady=10)

# middle main frame
class MiddleIdentifyFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='top', expand=True, fill='both', pady=15)
        self.config = config
        # self.cap = proj_camera()
        self.create_widgets()

    def create_widgets(self):
        self.middle_left = middle_left_identify_frame(self, self.config)
        self.middle_right = middle_right_identify_frame(self, self.config)

# middle left frame
class middle_left_identify_frame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='left', fill='both')
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        identify_boy_label = tk.Label(self, image=self.config["boy_img"], bg=self.config["BG_COLOR"])
        identify_boy_label.pack(padx=30, expand=True)

# middle right frame
class middle_right_identify_frame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(expand=True, fill='both')
        self.config = config
        #TODO: close camera
        # self.cap = proj_camera()
        self.create_widgets()

    def create_widgets(self):
        # video frame
        self.identify_video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.identify_video_label.pack(side='top', fill='both', expand=True)

        # prediction frame
        self.prediction_frame = tk.Frame(self, bg=self.config["BG_COLOR"], padx=10, pady=5)
        self.prediction_frame.pack(side="bottom", pady=0, padx=20, fill='x')
        self.prediction_label = tk.Label(self.prediction_frame, text="ז", bg=self.config["BG_COLOR"], font=("Calibri", 80, 'bold'))
        self.empty_frame = tk.Label(self.prediction_frame, width=int(self.prediction_frame.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame.pack(side='left', expand=True, fill='x')
        self.prediction_label.pack(side="left", pady=0)
        self.prediction_label_header = tk.Label(self.prediction_frame, image=self.config["meet_the_letter"], bg=self.config["BG_COLOR"],
                                                font=("Calibri", 40))
        self.prediction_label_header.pack(side='left', expand=True)
        self.config["cap"].start_camera(self.identify_video_label, self.prediction_label)

# bottom frame (not in use )
class bottom_identify_frame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.pack(side='bottom', expand=True, fill='x')
        self.create_widgets(config)

    def create_widgets(self, config):
        back_button = tk.Button(self, image=config["back_img"], bg=config["BG_COLOR"], borderwidth=0,
                                highlightbackground=config["BG_COLOR"], highlightcolor=config["BG_COLOR"], highlightthickness=0)
        back_button.pack(side='left', padx=30, pady=10)

# Main script
# root = tk.Tk()
# root.title("SignMyName")
# root.configure(bg='black')
# root.minsize(1200, 720)
# root.iconbitmap("assets/icon.ico")


# Create a configuration dictionary
# config = {
#     "BG_COLOR": "#FEE4FC",
#     "boy_img":  ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400, 500), Image.LANCZOS)),
#     "back_img": ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS)),
#     "meet_the_letter": ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((369, 80), Image.LANCZOS)),
#     "close_camera": lambda: None,  # Placeholder for close_camera function
#     "show_home_frame": lambda: None,  # Placeholder for show_home_frame function
#     "video_label": tk.Label()  # Placeholder for video_label
# }


# # Create an instance of the IdentifyPage class
# identify_page = IdentifyPage(root, config)

# root.mainloop()