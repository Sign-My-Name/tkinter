import tkinter as tk
import os
import pygame
from PIL import Image, ImageTk, ImageOps
from proj_camera import proj_camera
from proj_logger import get_logger

# Main NameBreakdown Frame
class LearnALetterPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info('Initializing LearnALetterPage...')
        self.config = config
        self.check_prediction_flag = 1
        self.config["check_prediction_flag"] = self.check_prediction_flag
        self.config["show_congrats"] = 0
        self.config["logger"] = self.logger
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.top_frame = TopFrame(self, self.config)
        self.middle_frame = MiddleFrame(self, self.config)
        self.bottom_frame = BottomFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        self.config["cap"].close_camera()
        self.config["check_prediction_flag"] = 0
        self.pack_forget()

# Top Frame
class TopFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.config["back_to_homepage"] = self.back_to_homepage
        self.what_your_name = config["whats_your_name_img"]
        self.only_hebrew_sound = pygame.mixer.Sound(f'sounds/only_hebrew.ogg')
        self.only_hebrew_sound.set_volume(3)
        self.letter = None
        self.config["letter"] = self.letter
        self.pack(side='top', fill='x')
        self.create_widgets()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='right', expand=True)

        self.name_label = tk.Label(self, image=self.what_your_name, font=("Calibri", 20), bg=self.config["BG_COLOR"])
        self.name_label.pack(side="right", padx=10)

        self.empty_frame2 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='left', expand=True)

        self.empty_frame3 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame3.pack(side='left', expand=True)

        self.submit_button = tk.Button(self, image=self.config["submit_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                       command=self.submit_name, highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                       highlightthickness=0, activebackground=self.config["BG_COLOR"], cursor="hand2")
        self.submit_button.pack(side="left", padx=10)


        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self, font=("Calibri", 20), justify="center", width=10, textvariable = self.entry_text)
        self.entry.pack(side="left", padx=10)

        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:1])

        self.entry_text.trace_add("write", lambda *args: character_limit(self.entry_text))



    def submit_name(self):
        self.letter = self.entry_text.get()
        if self.letter not in 'אבגדהוזחטיכךלמםנןסעפףצץקרשת' or self.letter == '':  
            self.parent.middle_frame.middle_left_frame.letter_boy_label.config(image = self.config['learn_a_letter_only_hebrew'])
            self.parent.middle_frame.middle_left_frame.display_letter('error')
            self.only_hebrew_sound.play()
            
        else:
            if self.letter == "ך":
                self.letter = "כ"
            elif self.letter == "ם":
                self.letter = "מ"
            elif self.letter == "ן":
                self.letter = "נ"
            elif self.letter == "ץ":
                self.letter = "צ"
            elif self.letter == "ף":
                self.letter = "פ"

            self.parent.middle_frame.middle_left_frame.letter_boy_label.config(image = self.config['learn_a_letter_boy'])
            self.config["letter"] = self.letter
            self.parent.middle_frame.middle_right_frame.try_again_flag = 0
            self.parent.middle_frame.middle_left_frame.display_name(self.letter)
            self.parent.middle_frame.middle_right_frame.check_prediction()
        


    def back_to_homepage(self):
        self.parent.close_frame()
        self.config["homePage_show"]()



class MiddleFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.middle_left_frame = MiddleLeftFrame(self, self.config)
        self.middle_right_frame = MiddleRightFrame(self, self.config)
        self.pack(expand=True, fill="both")


class MiddleRightFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.pack(side='right')
        self.try_again_sound = pygame.mixer.Sound(f'sounds/try_again.ogg')
        self.try_again_sound.set_volume(3)
        self.frame_count = 0
        self.try_again_flag = 0
        self.try_again_count = 0
        self.try_again_freq = 12
        self.create_widgets()

    def create_widgets(self):
        self.empty_frame1 = tk.Label(self, height=int(self.winfo_height() / 2),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame1.pack(side='bottom', expand=True)

        self.empty_frame2 = tk.Label(self, width=int(self.winfo_width() / 10),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame2.pack(side='left', expand=True)
        self.learn_a_letter_video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.learn_a_letter_video_label.pack(side='left', padx=8, fill='both', expand=True)
        self.prediction_label = tk.Label(self, text="", bg=self.config["BG_COLOR"],
                                         font=("Calibre", 80, 'bold'))
        self.config["cap"].start_camera(self.learn_a_letter_video_label, self.prediction_label, "letters")
    
    def check_prediction(self):
        
        self.frame_count += 1
        if self.config["letter"] == self.prediction_label.cget("text") and self.config['letter'] != '':
            self.config["logger"].info(f'the prediction is currect')
            self.config["letter"] = ""
            self.parent.middle_left_frame.display_letter("congrats")
            self.try_again_flag = 1
            self.parent.middle_left_frame.letter_boy_label.config(image=self.config['learn_a_letter_boy'])
            return
        else:
            if self.frame_count % self.try_again_freq == 0 and self.prediction_label.cget("text") != '':
                if self.try_again_flag == 0:
                    self.config['logger'].info(f'playing trying again sound')
                    self.try_again_sound.play()
                    self.try_again_flag = 1
                self.parent.middle_left_frame.letter_boy_label.config(image = self.config['learn_a_letter_try_again'])
                self.try_again_count += 1
                
            if self.try_again_count % 5 == 0:
                self.parent.middle_left_frame.letter_boy_label.config(image=self.config['learn_a_letter_boy'])
                self.try_again_freq = 35 

        if self.config["check_prediction_flag"] == 0:
            return
        
        if self.frame_count == 1500:
                self.frame_count = 0
                self.try_again_freq = 12
        
        self.after(100, self.check_prediction)


# Middle Left Frame
class MiddleLeftFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.letter = None
        self.pack(side='left', expand=True, fill='both')
        self.empty = ImageTk.PhotoImage(Image.open("letters/empty.png").resize((300, 300), Image.LANCZOS))
        self.letter_label = tk.Label(self,image=self.empty, bg=self.config["BG_COLOR"])
        self.letter_label.pack(side="top")
        self.learn_a_letter_boy = self.config['learn_a_letter_boy']
        self.letter_boy_label = tk.Label(self, image=self.learn_a_letter_boy, bg=self.config["BG_COLOR"])
        self.letter_boy_label.pack(side="bottom")

    def display_name(self, letter):
        self.letter = letter
        self.name_letters = list(letter)
        if self.name_letters:
            self.display_letter(self.name_letters[0])

    def display_letter(self, letter):
        image_file = f"letters/{letter}.png"
        if os.path.exists(image_file):
            image = Image.open(image_file)
            image = ImageOps.exif_transpose(image)  # Rotate the image based on EXIF metadata
            image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
            self.letter_label.config(image=image, fg="black")  # Reset the foreground color
            self.letter_label.image = image  # Keep a reference to prevent garbage collection
        else:
            self.letter_label.config(text=letter, image="", font=("Calibri", 34))


# Bottom Frame
class BottomFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side='bottom', fill='x')

        self.create_widgets()

    def return_to_homepage(self):
        self.config["back_to_homepage"]()

    def create_widgets(self):
        self.back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                     command=self.return_to_homepage,
                                     highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"],
                                     highlightthickness=1, activebackground=self.config["BG_COLOR"], cursor="hand2")
        self.back_button.pack(side="right", padx=10)

