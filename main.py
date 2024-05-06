from proj_logger import get_logger
logger = get_logger()

logger.info(f"initializing imports: cv2, numpy, tkinter, PIL, asyncio")
import tkinter as tk
from PIL import Image, ImageTk 
logger.info(f"initializing imports: os, threading, git, json")
import threading

BG_COLOR = "#FEE4FC"
No_hands_flag = 0

logger.info(f"initializing tkinter")
# Create the main window
root = tk.Tk()
root.title("SignMyName")
root.configure(bg=BG_COLOR)  # Set the background color
root.minsize(1200, 720)  # Set the minimum window size


logger.info("Checking for updates")
loaded_model = check_for_updates()



logger.info(f"initialazing locks")
lock_prediction = threading.Lock()
lock_queue = threading.Lock()



logger.info(f"initialazing global vars")
cap = None
camera_thread = None
keep_running = False
frame_counter = 0
prediction = ""

# Load images
logger.info(f"initialazing images")
logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((470, 190), Image.LANCZOS))
boy_img = ImageTk.PhotoImage(Image.open("assets/boy.png").resize((350, 350), Image.LANCZOS))
five_img = ImageTk.PhotoImage(Image.open("assets/five.png").resize((150, 145), Image.LANCZOS))
het_img = ImageTk.PhotoImage(Image.open("assets/het.png").resize((150, 145), Image.LANCZOS))
shin_img = ImageTk.PhotoImage(Image.open("assets/shin.png").resize((150, 145), Image.LANCZOS))
back_img = ImageTk.PhotoImage(Image.open("assets/back.png").resize((124, 67), Image.LANCZOS))
submit_img = ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS))
next_img = ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS))

# Create frames for the grid layout for home_page

video_label = tk.Label(root, bg=BG_COLOR)

### frame contol region

def show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame):
    global video_label
    video_label.pack_forget()

    home_top_frame.pack_forget()
    home_middle_frame.pack_forget()
    home_bottom_frame.pack_forget()


    video_label = tk.Label(identify_middle_frame, bg=BG_COLOR)
    identify_top_frame.pack()
    identify_middle_frame.pack(pady=10)
    identify_bottom_frame.pack(pady=10)
    video_label.pack(side="right", padx=10)

def show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame):
    global video_label
    video_label.pack_forget()

    home_top_frame.pack_forget()
    home_middle_frame.pack_forget()
    home_bottom_frame.pack_forget()

    video_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR)

    name_breakdown_top_frame.pack(pady=10)
    name_breakdown_middle_frame.pack(pady=10)
    name_breakdown_bottom_frame.pack(pady=10)
    video_label.pack(pady=10, fill='both', expand='true')

def show_build_a_word_frame(home_top_frame, home_middle_frame, home_bottom_frame):
    global video_label
    video_label.pack_forget()

    home_top_frame.pack_forget()
    home_middle_frame.pack_forget()
    home_bottom_frame.pack_forget()

    video_label = tk.Label(build_a_word_middle_frame, bg=BG_COLOR)
    
    build_a_word_top_frame.pack(pady=10)
    build_a_word_middle_frame.pack(pady=10)
    build_a_word_bottom_frame.pack(pady=10)
    video_label.pack(pady=10, fill='both', expand='true')

    building_words()

def show_home_frame(middle_frame=None, bottom_frame=None, video_label=None, top_frame=None):
    if top_frame:
        top_frame.pack_forget()
    if middle_frame:
        middle_frame.pack_forget()
    if bottom_frame:
        bottom_frame.pack_forget()
    if video_label:
        video_label.pack_forget()

    home_top_frame.pack(pady=10)
    home_middle_frame.pack()
    home_bottom_frame.pack(pady=10)
    return

### end frame control region

def update_prediction_label():
    return

logger.info(f"starting app")
root.mainloop()