import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from UI.identify_page import IdentifyPage
from UI.wrd_identify_page import WordIdentifyPage
from UI.learn_a_letter import LearnALetterPage
from UI.sign_a_word_page import SignAWordPage
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
        self.back_img = self.config["back_img"]
        self.identify_config = None
        self.word_identify_config = None
        
        self.create_widgets()

    def show_loading_popup(self):
        self.loading_popup = tk.Toplevel(self)
        self.loading_popup.title("Loading")
        ttk.Label(self.loading_popup, text="...טוען", font=("Guttman Yad-Brush", 50, 'bold')).pack(pady=20)

        self.loading_popup.update_idletasks()
        width = self.loading_popup.winfo_width()
        height = self.loading_popup.winfo_height()
        
        root_x = self.config['root'].winfo_rootx()
        root_y = self.config['root'].winfo_rooty()
        root_width = self.config['root'].winfo_width()
        root_height = self.config['root'].winfo_height()
        
        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)

        self.loading_popup.geometry(f"{400}x{200}+{x}+{y}")
        self.loading_popup.grab_set()
        self.loading_popup.update()


    def close_loading_popup(self):
        if self.loading_popup:
            self.loading_popup.destroy()

    def show_identify_page(self):
        self.config["root"].config(cursor='exchange')
        self.show_loading_popup()
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
        self.config["root"].config(cursor='')
        self.close_loading_popup()


    def show_word_identify_page(self):
        self.word_identify_config = {
            "BG_COLOR": "#dd6b62",
            "boy_img": self.identify_boy_img,
            "back_img": self.back_img,
            "meet_the_letter": self.meet_the_letter,
            "homePage_show": self.config["homePage_show"]
        }
        self.word_identify_page = WordIdentifyPage(self.config["root"], self.word_identify_config)
        self.config["homePage_forget"]()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        left_button = tk.Button(self, image=self.config["identify_img"], bg=self.config["BG_COLOR"],
                                 borderwidth=0, command=self.show_identify_page,  activebackground=self.config["BG_COLOR"], cursor="hand2")
        left_button.pack(side='top')
        self.empty_frame2 = tk.Label(self, image=self.config["spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='top', expand=True)
        left_bottom_button = tk.Button(self, image=self.config["word_identify_img"], bg=self.config["BG_COLOR"],
                                        borderwidth=0, command=self.show_word_identify_page, activebackground=self.config["BG_COLOR"], cursor="hand2")
        left_bottom_button.pack(pady=10, side='bottom')
        


# right frame
class RightHomeFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side="left", padx=10)
        self.identify_page = None
        self.word_identify_page = None
        self.create_widgets()

        # learn a letter images
        self.submit_img = self.config["submit_img"]
        self.back_img = self.config["back_img"]
        self.identify_boy_img = self.config["identify_boy"]
        self.meet_the_letter = self.config["meet_the_letter"]
        self.what_your_name_img = self.config["what_your_name_img"]
        
    def show_learnaletter(self):
        self.learn_a_letter_config = {
            "BG_COLOR": "#a8f4f6",
            "submit_img": self.submit_img,
            "back_img": self.back_img,
            "whats_your_name_img" : self.what_your_name_img,
            "homePage_show": self.config["homePage_show"]
        }
        self.learn_a_letter = LearnALetterPage(self.config["root"], self.learn_a_letter_config)
        self.config["homePage_forget"]()

    def show_signaword(self):
        self.sign_a_word_config =  {
            "BG_COLOR": "#eed4ff",
            "back_img": self.back_img,
            "boy_img": self.identify_boy_img,
            "homePage_show": self.config["homePage_show"]
        }

        self.sign_a_word = SignAWordPage(self.config["root"], self.sign_a_word_config)
        self.config["homePage_forget"]()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, image=self.config["top_spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='top', expand=True)
        right_top_button = tk.Button(self, image=self.config["learn_a_letter_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0, command=self.show_learnaletter, activebackground=self.config["BG_COLOR"], cursor="hand2")
        right_top_button.pack(side="top")
        self.empty_frame2 = tk.Label(self, image=self.config["spacer"],
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='top', expand=True)
        right_bottom_button = tk.Button(self, image=self.config["sign_a_word_img"], bg=self.config["BG_COLOR"],
                                borderwidth=0,  command=self.show_signaword, activebackground=self.config["BG_COLOR"], cursor="hand2")
        right_bottom_button.pack(pady=10, side='bottom')

