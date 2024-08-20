import threading
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

from collections import deque
from proj_camera import proj_camera
from proj_logger import get_logger

class frame_q:
    """
    Queue implementation with thread-safe operations.
    """
    def __init__(self):
        """
        Initializes the frame queue with a maximum length and lock.
        """
        self.q = deque(maxlen=1000000)
        self.lock = threading.Lock()
        self.logger = get_logger()

    def clear(self):
        """
        Clears the queue.
        """
        self.q.clear()

    def push(self, val):
        """
        Pushes a value to the queue in a thread-safe manner.
        """
        try:
            with self.lock:
                self.q.appendleft(val)

        except Exception:
            self.logger.error(f'Error: Push to q locked')

    def pop(self):
        """
        Pops a value from the queue in a thread-safe manner.
        """
        try:
            with self.lock:
                popped = self.q.pop()
            return popped
        
        except Exception:
            self.logger.error(f'Error: Pop to q locked')
            return False


class full_word:
    """
    Class for handling the construction and manipulation of a full word.
    """
    def __init__(self):
        """
        Initializes an empty word list.
        """
        self.word = []
        self.len = 0

    def clear(self):
        """
        Clears the word list.
        """
        self.word.clear()

    def append(self, char):
        """
        Appends a character to the word list if it's not a duplicate.
        """
        if len(self.word) > 0 and char == self.word[-1]:
            return
        if char != '?':
            self.len += 1
        self.word.append(char)

    def get_len(self):
        """
        Returns the length of the current word.
        """
        return self.len
    
    def print(self):
        """
        Returns the word as a string, excluding placeholder characters.
        """
        string = ''
        for i in self.word:
            if i == '?':
                continue
            string += i
        return string

    def backspace(self):
        """
        Removes the last character from the word.
        """
        if len(self.word) > 0:
            char = self.word.pop()
            if char == '?' and len(self.word) > 0:
                self.word.pop()
            if self.len > 0:
                self.len -= 1

class SignAWordPage(tk.Frame):
    """
    Main frame for the Sign A Word Page, responsible for initializing camera and UI components.
    """
    def __init__(self, parent, config):
        """
        Initializes the SignAWordPage with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.logger = get_logger()
        self.logger.info('Initializing SignAWordPage...')
        self.config = config
        self.config['logger'] = self.logger
        self.cap = proj_camera()
        self.config["cap"] = self.cap
        self.prediction_queue = frame_q()
        self.config["prediction_queue"] = self.prediction_queue
        self.top_frame = SignAWordTopFrame(self, self.config)
        self.middle_frame = SignAWordMiddleFrame(self, self.config)
        self.bottom_frame = SignAWordBottomFrame(self, self.config)
        self.pack(expand=True, fill='both')

    def close_frame(self):
        """
        Closes the SignAWordPage and stops the camera.
        """
        self.config["cap"].close_camera()
        self.pack_forget()
        self.config["homePage_show"]()

class SignAWordTopFrame(tk.Frame):
    """
    Top frame of the Sign A Word Page, containing the display for the current letter and completed word.
    """
    def __init__(self, parent, config):
        """
        Initializes the top frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.parent = parent
        self.config = config
        self.pack(side='top', fill='x')
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the top frame.
        """
        self.current_letter_label = tk.Label(self, image=self.config['finished_word'],
                                    bg=self.config["BG_COLOR"], font=("Calibri", 20))
        self.current_letter_label.pack(side='right', padx=20)

        self.completed_word_letter = tk.Label(self, text='', bg=self.config["BG_COLOR"], font=("Calibri", 70))
        self.completed_word_letter.pack(side='right', padx=20)

        build_a_word_back_button = tk.Button(self, image=self.config["back_space"], bg=self.config["BG_COLOR"], borderwidth=0,
                                             highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"], highlightthickness=0,
                                             command=self.back_sapce, activebackground=self.config["BG_COLOR"], cursor="hand2")
        build_a_word_back_button.pack(side='left', padx=15)

    def back_sapce(self):
        """
        Triggers the backspace functionality in the middle right frame.
        """
        self.parent.middle_frame.middle_right_frame.backspace = 1

class SignAWordMiddleFrame(tk.Frame):
    """
    Middle frame of the Sign A Word Page, containing the main interaction areas.
    """
    def __init__(self, parent, config):
        """
        Initializes the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"]) 
        self.config = config
        self.parent = parent
        self.pack(expand=True, fill="both")
        self.empty_frame = tk.Label(self, height=int(self.winfo_height()),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame.pack(side='left', expand=True)
        self.middle_left_frame = SignAWordMiddleLeftFrame(self, config)
        self.middle_right_frame = SignAWordMiddleRightFrame(self, config)

class SignAWordMiddleLeftFrame(tk.Frame):
    """
    Left section of the middle frame, displaying the instructional image.
    """
    def __init__(self, parent, config):
        """
        Initializes the left section of the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.pack(side='left', fill='both')

        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the left section of the middle frame.
        """
        self.empty_frame = tk.Label(self, height=int(self.winfo_height()),
                                    bg=self.config["BG_COLOR"])
        self.empty_frame.pack(side='top', expand=True)

    

        self.boy_img_label =tk.Label(self, image= self.config['sign_a_word_boy'], bg = self.config['BG_COLOR']) 
        self.boy_img_label.pack(side='bottom')


class SignAWordMiddleRightFrame(tk.Frame):
    """
    Right section of the middle frame, displaying the video feed and handling word construction.
    """
    def __init__(self, parent, config):
        """
        Initializes the right section of the middle frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.backspace = 0
        self.pack(side='right', fill='both')

        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the right section of the middle frame.
        """
        self.video_label = tk.Label(self, bg=self.config["BG_COLOR"])
        self.video_label.pack(side='right', padx=8)
        self.prediction_label = tk.Label(self, text='ממלא מקום',justify='center', bg=self.config["BG_COLOR"], font=("Calibri", 80, 'bold'))


        self.config["cap"].start_camera(self.video_label, self.prediction_label, "letters", self.config["prediction_queue"])

        self.building_words()

    def building_words(self):
        """
        Manages the word construction process by analyzing predictions from the camera feed.
        Uses a sliding window technique to accumulate character predictions and build the final word.
        """
        word = full_word()
        word.clear()
        prediction_queue = self.config["prediction_queue"]
        window_size = 7
        window_step = 3
        window = []
        prediction_queue.clear()

        def rolling_window_append(window):
            """
            Adds predictions to the sliding window until it reaches the specified size.
            Logs the current state of the window.
            """
            while len(prediction_queue.q) > 0 and len(window) < window_size:
                self.config['logger'].info(f'Window is {window}')
                window.append(prediction_queue.pop())
            return window

        def word_print():
                """
                Converts the accumulated characters into a string and updates the UI.
                Clears the prediction queue and the window for the next gesture.
                """
                string = word.print()
                self.config['logger'].info(f'the string created is: {string}')
                prediction_queue.clear()
                window.clear()
                self.parent.parent.top_frame.completed_word_letter.config(text=string)

        def rolling_window_check(window):
            """
            Determines the most frequent character in the sliding window.
            Uses a threshold to decide if a character is valid based on its frequency.
            """
            threshold = 0.5
            window = rolling_window_append(window)
            maxCountChar = ('', 0)
            if len(window) >= window_size:
                self.config['logger'].info(f'enough chars in window, getting max chat count')
                for charName in list(set(window)):
                    charCount = window.count(charName)

                    if charCount > maxCountChar[1]:
                        maxCountChar = (charName, charCount)

                if maxCountChar[1] / window_size < threshold:
                    maxCountChar = ('', 0)
                window = window[window_step - 1:]
                self.config['logger'].info(f'found char {charName}, changing window size to {len(window)}')

            return maxCountChar[0], window
        
        def get_word(window):
            """
            Continuously processes the prediction queue and appends valid characters to the word.
            Handles backspace operations and limits the word length to 10 characters.
            """
            if self.backspace == 1:
                word.backspace()
                window = []
                word_print()
                self.backspace = 0

            if word.get_len() < 10:
                if len(prediction_queue.q) > 0:
                    if prediction_queue.q[-1] == '?':
                        self.config['logger'].info(f'add ? into word')
                        char_name = '?'
                        prediction_queue.clear()
                        window.clear()
                    else:
                        char_name, window = rolling_window_check(window)
                    if char_name != '':
                        word.append(char_name)
                        word_print()

                        self.config['logger'].info(f'the window is {window} and the oldChars is: {word.word}')

            self.after(100, get_word, window)

        get_word(window)


class SignAWordBottomFrame(tk.Frame):
    """
    Bottom frame of the Sign A Word Page, containing navigation controls.
    """
    def __init__(self, parent, config):
        """
        Initializes the bottom frame with given configuration.
        """
        super().__init__(parent, bg=config["BG_COLOR"])
        self.config = config
        self.parent = parent
        self.pack(side='bottom', fill='x')
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets in the bottom frame.
        """
        build_a_word_back_button = tk.Button(self, image=self.config["back_img"], bg=self.config["BG_COLOR"], borderwidth=0,
                                             highlightbackground=self.config["BG_COLOR"], highlightcolor=self.config["BG_COLOR"], highlightthickness=0,
                                             command=self.parent.close_frame, activebackground=self.config["BG_COLOR"], cursor="hand2")
        build_a_word_back_button.pack(side='right', padx=15)
