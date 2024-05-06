import tkinter as tk
from PIL import Image, ImageTk 

# main identify Frame
class IdentifyPage(tk.Frame):
    def __init__(self, parent, BG_COLOR, boy_img, back_img, meet_the_letter, close_camera, show_home_frame, video_label):
        super().__init__(parent, bg=BG_COLOR)
        self.top_frame_identify = top_identify_frame(self, BG_COLOR, back_img)
        self.middle_frame_identify = middle_identify_frame(self, boy_img, meet_the_letter)
        # self.bottom_frame_identify = bottom_identify_frame(self, back_img)
        self.pack(expand= True, fill='both')
# end main identify frame

# top frame
class top_identify_frame(tk.Frame):
    def __init__(self, parent, BG_COLOR, back_img):
        super().__init__(parent,bg=BG_COLOR)
        self.pack(side='top', fill='x')
        self.create_widgets(back_img)
    
    def create_widgets(self, back_img):
        back_button = tk.Button(self, image=back_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0)
        back_button.pack(side='right', padx=30, pady=10)
# end top frame

# middle main frame
class middle_identify_frame(tk.Frame):
    def __init__(self, parent, boy_img, meet_the_letter):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(side='top',expand=True, fill='both', pady=15)

        self.create_widgets(boy_img, meet_the_letter)

    def create_widgets(self, boy_img, meet_the_letter):
        self.middle_left = middle_left_identify_frame(self, boy_img)
        self.middle_right = middle_right_identify_frame(self, meet_the_letter)
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
    def __init__(self, parent, meet_the_letter):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(expand=True, fill='both') 
        self.create_widgets(meet_the_letter)

    def create_widgets(self, meet_the_letter):
        #video frame
        video_placeholder = tk.Label(self,bg=BG_COLOR, image=placeholder_img)
        video_placeholder.pack(side='top', fill='both', expand=True)

        #prediction frame
        prediction_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=5)
        prediction_frame.pack(side="bottom", pady=0, padx=20, fill='x')
        prediction_label = tk.Label(prediction_frame, text="ז", bg=BG_COLOR, font=("Calibri", 80, 'bold'))
        empty_frame = tk.Label(prediction_frame, width=int(prediction_frame.winfo_width()/10), bg=BG_COLOR)
        empty_frame.pack(side='left', expand=True, fill='x')
        prediction_label.pack(side="left", pady=0)
        prediction_label_header = tk.Label(prediction_frame, image=meet_the_letter, bg=BG_COLOR, font=("Calibri", 40))
        prediction_label_header.pack(side='left', expand=True)
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

## temp empty root for testing
root = tk.Tk()
root.title("SignMyName")
root.configure(bg='black')  # Set the background color
root.minsize(1200, 720)
root.iconbitmap("assets/icon.ico")
BG_COLOR = "#FEE4FC"

# in place of the live video
placeholder_img = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640, 480), Image.LANCZOS))

# input images for class
boy_bubble_img = ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400,500),Image.LANCZOS))
back_button = ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS))
meet_the_letter = ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((369, 80), Image.LANCZOS))

## need to be in use!
video_label = tk.Label()

# place holder for proj_camera
def close_camera():
    pass

def show_home_frame():
    pass

# Create an instance of the IdentifyPage class 
identify_page = IdentifyPage(root, BG_COLOR, boy_bubble_img, back_button, meet_the_letter, close_camera, show_home_frame, video_label)

root.mainloop()