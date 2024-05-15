import tkinter as tk
from PIL import ImageTk, Image
from identify_page import IdentifyPage


##TODO: delete this, its for testig
import mediapipe as mp
import tensorflow as tf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# main HomePage Frame
class HomePage(tk.Frame):      
    def __init__(self, parent, BG_COLOR, logo_img, name_break_down_img, home_page_boy_img, identify_img, word_identify_img, sign_a_word_img):
        super().__init__(parent, bg=BG_COLOR)
        self.root = parent
        self.top_frame = TopHomeFrame(self,self.root, BG_COLOR, logo_img)
        self.middle_frame = MiddleHomeFrame(self,self.root, self.homePage_forget, self.homePage_show, BG_COLOR, name_break_down_img, home_page_boy_img, identify_img, word_identify_img, sign_a_word_img)
        # self.bottom_frame = BottomHomeFrame(self, BG_COLOR)
        self.pack(expand=True, fill='both')

    def homePage_forget(self):
        self.top_frame.pack_forget()
        self.middle_frame.pack_forget()
        self.pack_forget()

    def homePage_show(self):
        self.top_frame.pack(side='top', fill='x', pady=2)
        self.middle_frame.pack()
        self.pack(expand=True, fill='both')

# end main HomePage Frame

# top frame
class TopHomeFrame(tk.Frame):
    def __init__(self, parent, root, BG_COLOR, logo_img):
        super().__init__(parent, bg=BG_COLOR)
        self.root = root
        self.pack(side='top', fill='x', pady=2)
        self.create_widgets(logo_img)

    def create_widgets(self, logo_img):
        logo_label = tk.Label(self, image=logo_img, bg=BG_COLOR)
        logo_label.pack(side='top', fill='x')

# end top frame

# middle frame
class MiddleHomeFrame(tk.Frame):
    def __init__(self, parent, root, homepage_foget,homePage_show,  BG_COLOR, het_img, boy_img, identify_img, left_bottom_img, right_bottom_img):
        super().__init__(parent, bg=BG_COLOR)  # BG_COLOR
        self.root = root
        self.pack()
        self.create_widgets(BG_COLOR, self.root, homepage_foget, homePage_show,  het_img, boy_img, identify_img, left_bottom_img, right_bottom_img)

    def create_widgets(self, BG_COLOR, root, homepage_foget, homePage_show,  het_img, boy_img, identify_img, left_bottom_img, right_bottom_img):
        self.left_frame = LeftHomeFrame(self, root, homepage_foget, BG_COLOR, het_img, left_bottom_img)
        boy_label = tk.Label(self, image=boy_img, bg=BG_COLOR)  # BG_COLOR
        boy_label.pack(side="left")
        self.right_frame = RightHomeFrame(self, root, homepage_foget, homePage_show,  BG_COLOR, identify_img, right_bottom_img)

# end middle frame

# left frame
class LeftHomeFrame(tk.Frame):
    def __init__(self, parent, root, homepage_foget, BG_COLOR, het_img, left_bottom_img):
        super().__init__(parent, bg=BG_COLOR)  # BG_COLOR
        self.root = root
        self.pack(side="left")
        self.create_widgets(self.root,homepage_foget, BG_COLOR, het_img, left_bottom_img)

    def create_widgets(self, root, homepage_foget,  BG_COLOR, het_img, left_bottom_img):
        left_button = tk.Button(self, image=het_img, bg=BG_COLOR, borderwidth=0)
        left_button.pack()
        left_bottom_button = tk.Button(self, image=left_bottom_img, bg=BG_COLOR)
        left_bottom_button.pack(pady=10)
        
# end left frame

# right frame
class RightHomeFrame(tk.Frame):
    def __init__(self, parent, root, homepage_foget, homePage_show,  BG_COLOR, identify_img, right_bottom_img):
        super().__init__(parent, bg=BG_COLOR)
        self.root = root
        self.homepage_foget = homepage_foget
        self.homePage_show = homePage_show
        self.pack(side="left", padx=10)
        self.identify_page = None
        # Create a configuration dictionary
        self.config = {
            "BG_COLOR": "#FEE4FC",
            "boy_img":  identify_boy_bubble,
            "back_img": back_img,
            "meet_the_letter": meet_the_letter,
            "close_camera": lambda: None,  # Placeholder for close_camera function
            "show_home_frame": lambda: None,  # Placeholder for show_home_frame function
            "video_label": tk.Label() , # Placeholder for video_label
            "homePage_show": self.homePage_show
        }

        self.create_widgets( BG_COLOR, identify_img, right_bottom_img)
    
    ## TODO: add a root var that is passed down to the buttons
    def show_identify_page(self):
        print(f'in show_identify_page')
        self.identify_page = IdentifyPage(self.root, self.config)
        self.homepage_foget()
        # self.identify_page.show

    def create_widgets(self, BG_COLOR, identify_img, right_bottom_img):
        right_button = tk.Button(self, image=identify_img, command=lambda: [self.show_identify_page()], bg=BG_COLOR, borderwidth=0)
        right_button.pack()
        right_bottom_button = tk.Button(self, image=right_bottom_img, bg=BG_COLOR)
        right_bottom_button.pack(pady=10)
        

# end right frame

# bottom frame 
### NOT IN USE
class BottomHomeFrame(tk.Frame):
    def __init__(self, parent, BG_COLOR):
        super().__init__(parent, bg=BG_COLOR)  # BG_COLOR
        self.pack(pady=10)
        self.create_widgets(BG_COLOR)

    def create_widgets(self, BG_COLOR):
        welcome_label = tk.Label(self, text="!היי חברים, ברוכים הבאים", font=("Calibri", 34), bg=BG_COLOR, fg="black")
        welcome_label.pack(side='left', padx=30)

# end bottom frame



root = tk.Tk()
root.title("SignMyName")
root.configure(bg='black')  # Set the background color
root.minsize(1200, 720)
root.iconbitmap("assets/icon.ico")
# BG_COLOR = "#FEE4FC"
BG_COLOR = 'peach puff'



logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((423, 171), Image.LANCZOS))

home_page_boy_img = ImageTk.PhotoImage(Image.open("new_assets/homepage_boy.png").resize((450, 450), Image.LANCZOS))

word_identify_img = ImageTk.PhotoImage(Image.open("new_assets/WrdIdentify.png").resize((250, 250), Image.LANCZOS))
name_break_down_img = ImageTk.PhotoImage(Image.open("new_assets/NameBreakDown.png").resize((250, 250), Image.LANCZOS))
identify_img = ImageTk.PhotoImage(Image.open("new_assets/IdentifyPage.png").resize((250, 250), Image.LANCZOS))
sign_a_word_img = ImageTk.PhotoImage(Image.open("new_assets/SignAWord.png").resize((250, 250), Image.LANCZOS))

back_img = ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS))
submit_img = ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS))
next_img = ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS))

identify_boy_bubble = ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400, 500), Image.LANCZOS))
meet_the_letter = ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((250, 62), Image.LANCZOS))

home_page = HomePage(root, BG_COLOR, logo_img, name_break_down_img, home_page_boy_img, identify_img, word_identify_img, sign_a_word_img)

root.mainloop()


# home_top_frame.pack(pady=10)
# home_middle_frame.pack()
# home_bottom_frame.pack(pady=10)

# ### end region homepage