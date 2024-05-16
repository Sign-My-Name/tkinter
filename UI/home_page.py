import tkinter as tk
from PIL import ImageTk, Image
from UI.identify_page import IdentifyPage
from UI.name_breakdown_page import NameBreakdownPage
from proj_logger import get_logger

# main HomePage Frame
class HomePage(tk.Frame):      
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info(f'HomePage init...')
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
        self.name_breakdown_page = None

        #name breakdown images
        self.submit_img = self.config["submit_img"]
        self.back_img = self.config["back_img"]
        self.next_img = self.config["next_img"]
        self.name_breakdown_config = None
        self.create_widgets()

    def show_namebreakdown(self):
        self.name_breakdown_config = {
            "BG_COLOR": "#FEE4FC",
            "submit_img": self.submit_img,
            "back_img": self.back_img,
            "next_img": self.next_img,
            "homePage_show": self.config["homePage_show"]
        }
        self.name_breakdown_page = NameBreakdownPage(self.config["root"], self.name_breakdown_config)
        self.config["homePage_forget"]()

    def create_widgets(self):
        left_button = tk.Button(self, image=self.config["name_break_down_img"], bg=self.config["BG_COLOR"],
                                 borderwidth=0, command=self.show_namebreakdown)
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
        #identify image
        self.identify_boy_img = self.config["identify_boy_bubble"]
        self.meet_the_letter = self.config["meet_the_letter"]
        self.back_img = self.config["back_img"]
        self.identify_config = None
        
    def show_identify_page(self):
        self.identify_config = {
            "BG_COLOR": "#FEE4FC",
            "boy_img": self.identify_boy_img,
            "back_img": self.back_img,
            "meet_the_letter": self.meet_the_letter,
            "homePage_show": self.config["homePage_show"]
        }
        self.identify_page = IdentifyPage(self.config["root"], self.identify_config)
        self.config["homePage_forget"]()

    def create_widgets(self):
        right_button = tk.Button(self, image=self.config["identify_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0, command=self.show_identify_page)
        right_button.pack()
        right_bottom_button = tk.Button(self, image=self.config["word_identify_img"], bg=self.config["BG_COLOR"])
        right_bottom_button.pack(pady=10)

