import tkinter as tk
import json
from tkinter import ttk
from PIL import ImageTk, Image
from loadingPopup import LoadingPopup
from tooltip import Tooltip
from UI.identify_page import IdentifyPage
from UI.wrd_identify_page import WordIdentifyPage
from UI.learn_a_letter import LearnALetterPage
from UI.sign_a_word_page import SignAWordPage
from proj_logger import get_logger

with open('tooltips.json', 'r', encoding='utf-8') as file:
    tooltips = json.load(file)

# main HomePage Frame
class HomePage(tk.Frame):      
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info(f'HomePage init...')
        self.root = parent
        self.config = config
        self.config["root"] = self.root
        self.loading_popup = LoadingPopup(config["root"], config)
        self.config['loading_popup'] = self.loading_popup
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
        logo_label.pack(side='left', fill='x')


# middle frame
class MiddleHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.top_spacer = ImageTk.PhotoImage(Image.open("assets/spacer.png").resize((50, 180), Image.LANCZOS))
        self.config["top_spacer"] = self.top_spacer
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = LeftHomeFrame(self, self.config)
        self.middle_frame = tk.Frame(self, bg=self.config["BG_COLOR"])
        self.middle_frame.pack(side="left")
        boy_label = tk.Label(self.middle_frame, image=self.config["home_page_boy_img"], bg=self.config["BG_COLOR"])
        boy_label.pack(side="top")
        self.empty_frame = tk.Label(self.middle_frame, height=int(self.winfo_height()),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame.pack(side='top', expand=True)
        self.right_frame = RightHomeFrame(self, self.config)


# left frame
class LeftHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side="left")
        self.learn_a_letter = None
        #identify image
        self.identify_boy_img = self.config["identify_boy"]
        self.meet_the_letter = self.config["meet_the_letter"]
        self.word_identify_boy_img = self.config["word_identify_boy"]
        self.meet_the_word = config["meet_the_word"]
        self.back_img = self.config["back_img"]
        self.identify_config = None
        self.word_identify_config = None
        
        self.create_widgets()

    def show_identify_page(self):
        self.config['loading_popup'].show()
        self.identify_config = {
            "BG_COLOR": "#80b08f",
            "boy_img": self.identify_boy_img,
            "top_spacer" : ImageTk.PhotoImage(Image.open("assets/spacer.png").resize((50, 140), Image.LANCZOS)),
            "back_img": self.back_img,
            "meet_the_letter": self.meet_the_letter,
            "homePage_show": self.config["homePage_show"]
        }
        self.identify_page = IdentifyPage(self.config["root"], self.identify_config)
        self.config["homePage_forget"]()
        self.config['loading_popup'].close()


    def show_word_identify_page(self):
        self.config['loading_popup'].show()
        self.word_identify_config = {
            "BG_COLOR": "#dd6b62",
            "boy_img": self.word_identify_boy_img,
            "top_spacer" : ImageTk.PhotoImage(Image.open("assets/spacer.png").resize((50, 140), Image.LANCZOS)),
            "back_img": self.back_img,
            "meet_the_word": self.meet_the_word,
            "homePage_show": self.config["homePage_show"]
        }
        self.word_identify_page = WordIdentifyPage(self.config["root"], self.word_identify_config)
        self.config["homePage_forget"]()
        self.config["root"].config(cursor='')
        self.config['loading_popup'].close()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        left_button = tk.Button(self, image=self.config["identify_img"], bg=self.config["BG_COLOR"],
                                 borderwidth=0, command=self.show_identify_page,  activebackground=self.config["BG_COLOR"], cursor="hand2")
        left_button.pack(side='top')
        Tooltip(left_button, text=tooltips['left_button'], wraplength=300)
        self.empty_frame2 = tk.Label(self, image=self.config["spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='top', expand=True)
        left_bottom_button = tk.Button(self, image=self.config["word_identify_img"], bg=self.config["BG_COLOR"],
                                        borderwidth=0, command=self.show_word_identify_page, activebackground=self.config["BG_COLOR"], cursor="hand2")
        left_bottom_button.pack(pady=10, side='bottom')
        Tooltip(left_bottom_button, text=tooltips['left_bottom_button'], wraplength=300)
        


# right frame
class RightHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side="left", padx=10)
        self.identify_page = None
        self.word_identify_page = None
        self.create_widgets()
        self.back_img = self.config["back_img"]

        # learn a letter images
        self.submit_img = self.config["submit_img"]
        self.learn_a_letter_boy = self.config["learn_a_letter_boy"]
        self.learn_a_letter_try_again = self.config["learn_a_letter_try_again"]
        self.learn_a_letter_only_hebrew = self.config["learn_a_letter_only_hebrew"]
        self.meet_the_letter = self.config["meet_the_letter"]
        self.what_your_name_img = self.config["what_your_name_img"]

        # sign a word images
        self.sign_a_word_last_letter = self.config['last_letter']
        self.sign_a_word_finished_word = self.config['finished_word']
        self.sign_a_word_boy = self.config['sign_a_word_boy']
        self.back_space = self.config['backspace_img']
        
    def show_learnaletter(self):
        self.config['loading_popup'].show()
        self.learn_a_letter_config = {
            "BG_COLOR": "#a8f4f6",
            "submit_img": self.submit_img,
            "back_img": self.back_img,
            "whats_your_name_img" : self.what_your_name_img,
            "learn_a_letter_boy" : self.learn_a_letter_boy,
            "learn_a_letter_try_again" : self.learn_a_letter_try_again,
            "learn_a_letter_only_hebrew" : self.learn_a_letter_only_hebrew,
            "homePage_show": self.config["homePage_show"]
        }
        self.learn_a_letter = LearnALetterPage(self.config["root"], self.learn_a_letter_config)
        self.config["homePage_forget"]()
        self.config['loading_popup'].close()

    def show_signaword(self):
        self.config['loading_popup'].show()
        self.sign_a_word_config =  {
            "BG_COLOR": "#eed4ff",
            "back_img": self.back_img,
            "last_letter": self.sign_a_word_last_letter,
            "finished_word": self.sign_a_word_finished_word,
            "sign_a_word_boy": self.sign_a_word_boy,
            "back_space" : self.back_space,
            "homePage_show": self.config["homePage_show"]
        }

        self.sign_a_word = SignAWordPage(self.config["root"], self.sign_a_word_config)
        self.config["homePage_forget"]()
        self.config['loading_popup'].close()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        right_top_button = tk.Button(self, image=self.config["learn_a_letter_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0, command=self.show_learnaletter, activebackground=self.config["BG_COLOR"], cursor="hand2")
        right_top_button.pack(side="top")
        Tooltip(right_top_button, text=tooltips['right_button'], wraplength=300)
        self.empty_frame2 = tk.Label(self, image=self.config["spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='top', expand=True)
        right_bottom_button = tk.Button(self, image=self.config["sign_a_word_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0,  command=self.show_signaword, activebackground=self.config["BG_COLOR"], cursor="hand2")
        right_bottom_button.pack(pady=10, side='bottom')
        Tooltip(right_bottom_button, text=tooltips['right_bottom_button'], wraplength=300)

