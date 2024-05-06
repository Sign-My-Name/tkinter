import threading
import tkinter as tk
from collections import deque
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

class sign_a_word(tk.Frame):
    def __init__(self) -> None:
        pass


##### build a word frame

build_a_word_top_frame = tk.Frame(root, bg=BG_COLOR)
build_a_word_middle_frame = tk.Frame(root, bg=BG_COLOR)
build_a_word_bottom_frame = tk.Frame(root, bg=BG_COLOR)

build_a_word_header = tk.Label(build_a_word_top_frame, text="!בנה מילה", font=("Calibri", 20),  bg=BG_COLOR, fg="black")
build_a_word_header.pack(side="top")

build_a_word_back_button = tk.Button(build_a_word_top_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                             highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                             command=lambda: [close_camera(), show_home_frame(build_a_word_top_frame, build_a_word_middle_frame, build_a_word_bottom_frame, video_label)])
build_a_word_back_button.pack(side='right', padx=15)

build_a_word_boy_label = tk.Label(build_a_word_middle_frame, image=boy_img, bg=BG_COLOR)
build_a_word_boy_label.pack(side="left")

completed_word_frame = tk.Frame(build_a_word_bottom_frame, bg=BG_COLOR, padx=10, pady=5)
completed_word_frame.pack(padx=15, fill='both')


completed_word_current_letter = tk.Label(build_a_word_middle_frame, text='',  bg=BG_COLOR, font=("Calibri", 20))
completed_word_current_letter.pack(side='left', padx=50)

completed_word_label_header = tk.Label(build_a_word_middle_frame, text="אות נוכחית", bg=BG_COLOR, font=("Calibri", 20))
completed_word_label_header.pack(side='right', padx=50)

completed_word_word = tk.Label(completed_word_frame, text='',  bg=BG_COLOR, font=("Calibri", 20))
completed_word_word.pack(side='left', padx=50)

completed_word_label_header = tk.Label(completed_word_frame, text=":המילה שבנית", bg=BG_COLOR, font=("Calibri", 20))
completed_word_label_header.pack(side='right', padx=50)



def building_words(prediction_queue):
    global prediction, No_hands_flag
    prediction_queue = deque(maxlen=1000000) #TODO: how to reset the queue
    window_size = 7
    window_step = 3
    window = []
    
    def rolling_window_append(window):
        while  len(prediction_queue) > 0 and len(window) < window_size:
            print(f"filling window, {len(window)}, {len(prediction_queue)}")
            print(f'Window is {window}')
            window.append(q_pop())
        print('Finished while')
        return window
    
    def rolling_windows_char_change(old_chars,new_char):
        if len(old_chars) == 0 or old_chars[-1] != new_char:
            old_chars.append(new_char)
 

    def rolling_window_check(window):
        print(f'Window size is {len(window)}')
        window = rolling_window_append(window)
        maxCountChar = ('',0)
        if len(window) >= window_size:
            print('enough chars in window, getting max chat count')
            for charName in list(set(window)):
                charCount = window.count(charName)

                if charCount > maxCountChar[1]:
                    maxCountChar = (charName,charCount)
            window = window[window_step-1:]
            print(f'found char {charName}, changing window size to {len(window)}')

        return maxCountChar[0], window

    def get_word(window,old_chars=[]):
        completed_word_current_letter.config(text=prediction)
        # print('trying to get word')
        if len(prediction_queue) > 0:
            char_name, window = rolling_window_check(window)
            if char_name != '':
                rolling_windows_char_change(old_chars,char_name)
                print(f'the window is {window} and the oldChars is: {old_chars}')
        
        if No_hands_flag == 1:
            old_chars[::-1]
            string = ''
            for i in old_chars:
                string += i
            completed_word_word.config(text=string)
            old_chars = ''
            # No_hands_flag = 0

            return
        root.after(100, get_word, window, old_chars )

    get_word(window, [])
    


##### end build a word frame