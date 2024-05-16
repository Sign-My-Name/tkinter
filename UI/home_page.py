import tkinter as tk
from PIL import ImageTk, Image
from identify_page import IdentifyPage

import mediapipe as mp
import tensorflow as tf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# main HomePage Frame
class HomePage(tk.Frame):      
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.root = parent
        self.config = config
        self.config["root"] = self.root
        self.config["homePage_forget"] = self.homePage_forget
        self.config["homePage_show"] = self.homePage_show
        self.top_frame = TopHomeFrame(self, self.config)
        self.middle_frame = MiddleHomeFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def homePage_forget(self):
        self.top_frame.pack_forget()
        self.middle_frame.pack_forget()
        self.pack_forget()

    def homePage_show(self):
        self.top_frame.pack(side='top', fill='x', pady=2)
        self.middle_frame.pack()
        self.pack(expand=True, fill='both')


# top frame
class TopHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side='top', fill='x', pady=2)
        self.create_widgets()

    def create_widgets(self):
        logo_label = tk.Label(self, image=self.config["logo_img"], bg=self.config["BG_COLOR"])
        logo_label.pack(side='top', fill='x')


# middle frame
class MiddleHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = LeftHomeFrame(self, self.config)
        boy_label = tk.Label(self, image=self.config["home_page_boy_img"], bg=self.config["BG_COLOR"])
        boy_label.pack(side="left")
        self.right_frame = RightHomeFrame(self, self.config)


# left frame
class LeftHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side="left")
        self.create_widgets()

    def create_widgets(self):
        left_button = tk.Button(self, image=self.config["name_break_down_img"], bg=self.config["BG_COLOR"], borderwidth=0)
        left_button.pack()
        left_bottom_button = tk.Button(self, image=self.config["sign_a_word_img"], bg=self.config["BG_COLOR"])
        left_bottom_button.pack(pady=10)


# right frame
class RightHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side="left", padx=10)
        self.identify_page = None
        self.create_widgets()
        self.boy_img = self.config["identify_boy_bubble"]
        self.back_img = self.config["back_img"]
        self.meet_the_letter = self.config["meet_the_letter"]
        self.identify_config = {
            "BG_COLOR": "#FEE4FC",
            "boy_img": self.boy_img ,
            "back_img": back_img,
            "meet_the_letter": meet_the_letter,
            "homePage_show": self.config["homePage_show"]
        }
    def show_identify_page(self):
        self.identify_page = IdentifyPage(self.config["root"], self.identify_config)
        self.config["homePage_forget"]()

    def create_widgets(self):
        right_button = tk.Button(self, image=self.config["identify_img"], command=self.show_identify_page, bg=self.config["BG_COLOR"], borderwidth=0)
        right_button.pack()
        right_bottom_button = tk.Button(self, image=self.config["word_identify_img"], bg=self.config["BG_COLOR"])
        right_bottom_button.pack(pady=10)


# Set up the main application
root = tk.Tk()
root.title("SignMyName")
root.configure(bg='black')  # Set the background color
root.minsize(1200, 720)
root.iconbitmap("assets/icon.ico")
BG_COLOR = 'peach puff'


# logo image
logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((423, 171), Image.LANCZOS))

# all pages images
back_img = ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS))

# home page images
home_page_boy_img = ImageTk.PhotoImage(Image.open("new_assets/homepage_boy.png").resize((450, 450), Image.LANCZOS))
word_identify_img = ImageTk.PhotoImage(Image.open("new_assets/WrdIdentify.png").resize((250, 250), Image.LANCZOS))
name_break_down_img = ImageTk.PhotoImage(Image.open("new_assets/NameBreakDown.png").resize((250, 250), Image.LANCZOS))
identify_img = ImageTk.PhotoImage(Image.open("new_assets/IdentifyPage.png").resize((250, 250), Image.LANCZOS))
sign_a_word_img = ImageTk.PhotoImage(Image.open("new_assets/SignAWord.png").resize((250, 250), Image.LANCZOS))

# name breakdown iamges
submit_img = ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS))
next_img = ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS))

# identify page images
identify_boy_bubble = ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400, 500), Image.LANCZOS))
meet_the_letter = ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((250, 62), Image.LANCZOS))


# Load images and create configuration dictionary
config = {
    "BG_COLOR": BG_COLOR,
    "logo_img": logo_img,
    "home_page_boy_img": home_page_boy_img,
    "identify_img": identify_img,
    "word_identify_img": word_identify_img,
    "name_break_down_img": name_break_down_img,
    "sign_a_word_img": sign_a_word_img,
    "identify_boy_bubble" : identify_boy_bubble,
    "back_img" : back_img,
    "meet_the_letter" : meet_the_letter,
}

home_page = HomePage(root, config)

root.mainloop()
