import threading
import tkinter as tk
from collections import deque
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from proj_camera import proj_camera
from proj_logger import get_logger

class frame_q:
    def __init__(self):
        self.q = deque(maxlen=1000000)
        self.lock = threading.Lock()
        self.logger = get_logger()

    def push(self, val):
        try:
            self.lock.acquire()
            self.q.appendleft(val)
            self.lock.release()
        except Exception:
            self.logger.error(f'Error: Push to q locked')

    def pop(self):
        try:
            self.lock.acquire()
            popped = self.q.pop()
            self.lock.release()
            return popped
        except Exception:
            self.logger.error(f'Error: Pop to q locked')
            return False

class SignAWordPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info('Initializing SignAWordPage...')
        self.config = config
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.prediction_queue = frame_q()
        self.config["prediction_queue"] = self.prediction_queue
        self.top_frame = SignAWordTopFrame(self, self.config)
        self.middle_frame = SignAWordMiddleFrame(self, self.config)
        self.bottom_frame = SignAWordBottomFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        self.config["cap"].close_camera()
        self.pack_forget()
        self.config["homePage_show"]()

class SignAWordTopFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.pack(side='top', fill='x')
        self.create_widgets()

    def create_widgets(self):
        build_a_word_header = tk.Label(self, text="!בנה מילה", font=("Calibri", 20), bg=self.config["BG_COLOR"], fg="black")
        build_a_word_header.pack(side="top")

        build_a_word_back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                             highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"], highlightthickness=0,
                                             command=self.parent.close_frame, activebackground=self.config["BG_COLOR"])
        build_a_word_back_button.pack(side='right', padx=15)

class SignAWordMiddleFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        completed_word_frame = tk.Frame(self, bg=self.config["BG_COLOR"], padx=10, pady=5)
        completed_word_frame.pack(padx=15, fill='both')

        self.completed_word_current_letter = tk.Label(self, text='', bg=self.config["BG_COLOR"], font=("Calibri", 20))
        self.completed_word_current_letter.pack(side='left', padx=50)

        completed_word_label_header = tk.Label(self, text="אות נוכחית", bg=self.config["BG_COLOR"], font=("Calibri", 20))
        completed_word_label_header.pack(side='right', padx=50)

        self.completed_word_word = tk.Label(completed_word_frame, text='', bg=self.config["BG_COLOR"], font=("Calibri", 20))
        self.completed_word_word.pack(side='right', padx=50)

        completed_word_label_header = tk.Label(completed_word_frame, text=":המילה שבנית", bg=self.config["BG_COLOR"], font=("Calibri", 20))
        completed_word_label_header.pack(side='right', padx=50)

        self.video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.video_label.pack(side='right', fill='both', expand=True)

        self.prediction_label = tk.Label(self, text="", bg=self.config["BG_COLOR"], font=("Calibri", 80, 'bold'))

        self.config["cap"].start_camera(self.video_label, self.prediction_label, self.config["prediction_queue"])

        self.building_words()

    def building_words(self):
        global prediction, No_hands_flag
        prediction_queue = self.config["prediction_queue"]
        window_size = 7
        window_step = 3
        window = []

        def rolling_window_append(window):
            while len(prediction_queue.q) > 0 and len(window) < window_size:
                print(f"filling window, {len(window)}, {len(prediction_queue.q)}")
                print(f'Window is {window}')
                window.append(prediction_queue.pop())
            print('Finished while')
            return window

        def rolling_windows_char_change(old_chars, new_char):
            if len(old_chars) == 0 or old_chars[-1] != new_char:
                old_chars.append(new_char)

        def rolling_window_check(window):
            print(f'Window size is {len(window)}')
            window = rolling_window_append(window)
            maxCountChar = ('', 0)
            if len(window) >= window_size:
                print('enough chars in window, getting max chat count')
                for charName in list(set(window)):
                    charCount = window.count(charName)

                    if charCount > maxCountChar[1]:
                        maxCountChar = (charName, charCount)
                window = window[window_step - 1:]
                print(f'found char {charName}, changing window size to {len(window)}')

            return maxCountChar[0], window

        def get_word(window, old_chars=[]):
            No_hands_flag = 0
            # self.completed_word_current_letter.config(text=prediction)
            if len(prediction_queue.q) > 0:
                char_name, window = rolling_window_check(window)
                if char_name != '':
                    rolling_windows_char_change(old_chars, char_name)
                    print(f'the window is {window} and the oldChars is: {old_chars}')

            if No_hands_flag == 1:
                old_chars = old_chars[::-1]
                string = ''
                for i in old_chars:
                    string += i
                self.completed_word_word.config(text=string)
                old_chars = []
                No_hands_flag = 0

            self.after(100, get_word, window, old_chars)

        get_word(window, [])

class SignAWordBottomFrame(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.pack(side='bottom', fill='x')
        self.create_widgets()

    def create_widgets(self):
        pass