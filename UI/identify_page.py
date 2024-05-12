import tkinter as tk
import sys
import os
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proj_camera import proj_camera
from proj_logger import get_logger


# main identify Frame
class IdentifyPage(tk.Frame):
    def __init__(self, parent, BG_COLOR, boy_img, back_img, meet_the_letter, close_camera, show_home_frame,
                 video_label):
        super().__init__(parent, bg=BG_COLOR)
        self.logger = get_logger()
        self.logger.info(f'starting init of IdentifyPage')
        self.cap = proj_camera()
        self.top_frame_identify = TopIdentifyFrame(self, BG_COLOR, back_img)
        self.middle_frame_identify = MiddleIdentifyFrame(self, self.cap, boy_img, meet_the_letter)
        # self.bottom_frame_identify = bottom_identify_frame(self, back_img)

    def close_frame(self):
        self.cap.close_camera()
        self.pack_forget()
# end main identify frame

# top frame
class TopIdentifyFrame(tk.Frame):
    def __init__(self, parent, BG_COLOR, back_img):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(side='top', fill='x')
        self.create_widgets(back_img)

    def create_widgets(self, back_img):
        back_button = tk.Button(self, image=back_img, bg=BG_COLOR, borderwidth=0,
                                highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        back_button.pack(side='right', padx=30, pady=10)


# end top frame

# middle main frame
class MiddleIdentifyFrame(tk.Frame):
    def __init__(self, parent, cap, boy_img, meet_the_letter):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(side='top', expand=True, fill='both', pady=15)
        self.cap = cap
        self.create_widgets(boy_img, self.cap, meet_the_letter)

    def create_widgets(self, boy_img, cap, meet_the_letter):
        self.middle_left = middle_left_identify_frame(self, boy_img)
        self.middle_right = middle_right_identify_frame(self, cap, meet_the_letter)


# end middle main frame

# middle left frame
class middle_left_identify_frame(tk.Frame):
    def __init__(self, parent, boy_img):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(side='left', fill='both')
        self.create_widgets(boy_img)

    def create_widgets(self, boy_img):
        identify_boy_label = tk.Label(self, image=boy_img, bg=BG_COLOR)
        identify_boy_label.pack(padx=30, expand=True)


# end middle left frame

# middle right frame
class middle_right_identify_frame(tk.Frame):
    def __init__(self, parent, cap, meet_the_letter):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(expand=True, fill='both')
        self.cap = cap
        self.create_widgets(meet_the_letter)

    def create_widgets(self, meet_the_letter):
        # video frame
        self.identify_video_label = tk.Label(self, bg=BG_COLOR)
        self.identify_video_label.pack(side='top', fill='both', expand=True)

        # prediction frame
        self.prediction_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=5)
        self.prediction_frame.pack(side="bottom", pady=0, padx=20, fill='x')
        self.prediction_label = tk.Label(self.prediction_frame, text="ז", bg=BG_COLOR, font=("Calibri", 80, 'bold'))
        self.empty_frame = tk.Label(self.prediction_frame, width=int(self.prediction_frame.winfo_width() / 10),
                                    bg=BG_COLOR)
        self.empty_frame.pack(side='left', expand=True, fill='x')
        self.prediction_label.pack(side="left", pady=0)
        self.prediction_label_header = tk.Label(self.prediction_frame, image=meet_the_letter, bg=BG_COLOR,
                                                font=("Calibri", 40))
        self.prediction_label_header.pack(side='left', expand=True)
        self.cap.start_camera(self.identify_video_label, self.prediction_label)


# end middle right frame

# bottom frame (not in use )
class bottom_identify_frame(tk.Frame):
    def __init__(self, parent, back_img):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(side='bottom', expand=True, fill='x')

        self.create_widgets(back_img)

    def create_widgets(self, back_img):
        back_button = tk.Button(self, image=back_img, bg=BG_COLOR, borderwidth=0,
                                highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        back_button.pack(side='left', padx=30, pady=10)


# end bottom frame ( not in use )

# ## temp empty root for testing
# root = tk.Tk()
# root.title("SignMyName")
# root.configure(bg='black')  # Set the background color
# root.minsize(1200, 720)
# root.iconbitmap("assets/icon.ico")
BG_COLOR = "#FEE4FC"

# # in place of the live video
# placeholder_img = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640, 480), Image.LANCZOS))

# # input images for class
# boy_bubble_img = ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400, 500), Image.LANCZOS))
# back_button = ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS))
# meet_the_letter = ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((369, 80), Image.LANCZOS))

# ## need to be in use!
# video_label = tk.Label()


# # place holder for proj_camera
# def close_camera():
#     pass


# def show_home_frame():
#     pass


# # Create an instance of the IdentifyPage class
# identify_page = IdentifyPage(root, BG_COLOR, boy_bubble_img, back_button, meet_the_letter, close_camera,
#                              show_home_frame, video_label)

# root.mainloop()
