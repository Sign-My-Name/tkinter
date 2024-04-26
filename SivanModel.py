import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info(f"initializing imports: cv2, numpy, tkinter, PIL, asyncio")
import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageOps
logger.info(f"initializing imports: mediapipe")
import mediapipe as mp
logger.info(f"initializing imports: tensorflow, subprocess")
import tensorflow as tf
import subprocess
logger.info(f"initializing imports: os, threading, git, json")
import os
import threading
import json
import requests
from collections import deque

### KERAS ML RESGION
logger.info(f"initializing tensorflow's keras and model loading")
# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#check for updates for the model

def get_local_commit_hash():
    with open('conf.json', 'r') as file:
        config = json.load(file)
        return config['model_commit_hash']

local_commit_hash = get_local_commit_hash()

def get_latest_commit_hash():
    # Setup the API URL to fetch the latest commit from the main branch
    api_url = 'https://api.github.com/repos/Sign-My-Name/Model/commits/main'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    # Make the API request
    try:
        response = requests.get(api_url, headers=headers)
    except Exception:
        logger.info("No connection to Git API, continueing")
        return None
    if response.status_code == 200:
        data = response.json()
        return data['sha']
    else:
        print("Failed to fetch commit data")
        return None

def user_prompt_update():
    return messageWindow()

def update_commit_hash_in_config(latest_commit_hash):
    # Load the existing data from the file
    with open('conf.json', 'r') as file:
        config = json.load(file)
    
    # Update the commit hash
    config['model_commit_hash'] = latest_commit_hash
    
    # Write the updated data back to the file
    with open('conf.json', 'w') as file:
        json.dump(config, file, indent=4)

def update_model(progress_window, progress_bar, model_repo_path):
    try:
        os.makedirs(model_repo_path, exist_ok=True)
        if not os.path.exists(os.path.join(model_repo_path, '.git')):
            subprocess.run(['git', 'init'], cwd=model_repo_path, check=True)
            remote_repo_url = 'https://github.com/Sign-My-Name/Model.git'
            subprocess.run(['git', 'remote', 'add', 'origin', remote_repo_url], cwd=model_repo_path, check=True)
        
        subprocess.run(['git', 'pull', 'origin', 'main'], cwd=model_repo_path, check=True)
        logger.info("Model updated to the latest version.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to update the model: {e}")
    finally:
        return True
        
def check_for_updates():
    model_repo_path = '\SignMyNameSivan\model'
    local_commit_hash = get_local_commit_hash()
    latest_commit_hash = get_latest_commit_hash()
    
    if latest_commit_hash and local_commit_hash != latest_commit_hash:
        if user_prompt_update():
            update_commit_hash_in_config(latest_commit_hash)
            logger.info("Updating the model...")
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            progress_window = tk.Toplevel(root)
            progress_window.title("Updating Model")
            progress_window.geometry("400x100")  # Set the size of the window
            progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')
            progress_bar.pack(pady=20, padx=20) 
            progress_bar.pack(pady=20)
            progress_bar.start()

            update_thread = threading.Thread(target=update_model, args=(progress_window, progress_bar, model_repo_path))
            update_thread.start()
            
            while update_thread.is_alive():
                progress_window.update()
                progress_window.update_idletasks()
            
            progress_window.destroy()  # Close the progress window after the update completes
            root.destroy()  # Ensure root window is also closed to clean up all GUI components
        else:
            logger.info("Update cancelled by the user.")
    else:
        logger.info("Your model is up to date.")

    loaded_model_dir = os.path.join(model_repo_path, 'model.h5')
    return tf.keras.models.load_model(loaded_model_dir)

def messageWindow():
    win = tk.Toplevel()
    root.withdraw()
    win.title('יש עדכון')
    win.geometry("400x200")
    message = "קיים עדכון למערכת, תרצה לעדכן?"
    tk.Label(win, text=message).pack(pady=20)
    response = tk.BooleanVar(value=None)

    # Define button actions
    def yes_action():
        response.set(True)
        win.destroy()

    def no_action():
        response.set(False)
        win.destroy()

    tk.Button(win, text='כן', command=yes_action).pack(side=tk.LEFT, padx=50, pady=20)
    tk.Button(win, text='לא', command=no_action).pack(side=tk.RIGHT, padx=50, pady=20)

    win.wait_window()
    root.deiconify()  # Wait for the window to be destroyed
    return response.get()


# Load the trained model
# loaded_model_dir = r'ML/model/model.h5'
# loaded_model = tf.keras.models.load_model(loaded_model_dir)
class_to_letter = ['B', 'C', 'D', 'F', 'I', 'L', 'M', 'N', 'R', 'S', 'T', 'W', 'Z', 'nothing']
english_to_hebrew = {
    'B': 'ב', 'C': 'כ', 'D': 'ו', 'F': 'ט', 'I': 'י', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'R': 'ר', 'S': 'ס',
    'T': 'ת', 'W': 'ש', 'Z': 'ז'
}

hebrew_dict = {
    0: 'א', 1: 'ב', 2: 'ג', 3: 'ד', 4: 'ה', 5: 'ו', 6: 'ז', 7: 'ח', 8: 'ט', 9: 'י', 10: 'כ', 11: 'ל', 12: 'מ', 13: 'נ',  
    14: 'ס',
    15: 'ע', 16: 'פ', 17: 'צ', 18: 'ק', 19: 'ר', 20: 'ש', 21: 'ת'
}

hebrew_dict1 = {
    'א': 'ale', 'ב': 'bet', 'ג': 'gim', 'ד': 'dal', 'ה': 'hey', 'ו': 'vav', 'ז': 'zay', 'ח': 'het', 'ט': 'tet',
    'י': 'yud', 'כ': 'kaf',
    'ל': 'lam', 'מ': 'mem', 'נ': 'nun', 'ס': 'sam',
    'ע': 'ain', 'פ': 'pey', 'צ': 'tza', 'ק': 'kuf', 'ר': 'rey', 'ש': 'shi', 'ת': 'taf'
}

# Initialize the MediaPipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# prediction_queue = deque(maxlen=1000000)


def draw_hand_skeleton(image):
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        return annotated_image
    return image


def isolate_and_crop_hand(image, padding=60):
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        image = draw_hand_skeleton(image)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for hand_landmarks in results.multi_hand_landmarks:
            points = [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
                      for landmark in hand_landmarks.landmark]
            hull = cv2.convexHull(np.array(points))
            cv2.fillConvexPoly(mask, hull, 255)

            # Apply padding via dilation
            kernel = np.ones((padding * 2, padding * 2), np.uint8)
            padded_mask = cv2.dilate(mask, kernel, iterations=1)

            # Create a black background image
            black_background = np.zeros_like(image)

            # Isolate the hand by combining it with the black background
            isolated_hand = cv2.bitwise_and(image, image, mask=padded_mask)
            final_image = cv2.bitwise_or(black_background, isolated_hand)

            # Calculate bounding box for the isolated hand with padding
            x, y, w, h = cv2.boundingRect(padded_mask)
            x_start = max(x - padding, 0)
            y_start = max(y - padding, 0)
            x_end = min(x_start + w + 2 * padding, image.shape[1])
            y_end = min(y_start + h + 2 * padding, image.shape[0])

            # Crop the image to the bounding box with padding
            cropped_image = final_image[y_start:y_end, x_start:x_end]
            return cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    return None



def cut_image(image, size=None):
    image = image.astype(np.uint8)
    processed_image = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if processed_image.multi_hand_landmarks:
        hand_landmarks = processed_image.multi_hand_landmarks[0]
        x_coords = [landmark.x for landmark in hand_landmarks.landmark]
        y_coords = [landmark.y for landmark in hand_landmarks.landmark]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)


        val_to_adjust = max(image.shape[0], image.shape[1]) * 0.08

        x_min_adjust = int(x_min * image.shape[1] - val_to_adjust)
        y_min_adjust = int(y_min * image.shape[0] - val_to_adjust)
        x_max_adjust = int(x_max * image.shape[1] + val_to_adjust)
        y_max_adjust = int(y_max * image.shape[0] + val_to_adjust)
        if x_min_adjust < 0:
            x_min_adjust = max(int(x_min * image.shape[1] - 15), 0)
        if y_min_adjust < 0:
            y_min_adjust = max(int(y_min * image.shape[0] - 15), 0)

        image = image[y_min_adjust:y_max_adjust, x_min_adjust:x_max_adjust]
        hand_region_uint8 = image.astype(np.uint8)
        # hand_region_bgr = cv2.cvtColor(hand_region_uint8, cv2.COLOR_RGB2BGR)
        hand_region_bgr = cv2.resize(hand_region_uint8, dsize=size)
    else:
        hand_region_bgr = None
    return hand_region_bgr

def predict_image(image):
    if image is None:
        return "",0.0
    # Make a prediction on the single image
    image = np.expand_dims(image, axis=0)
    raw_pred = loaded_model.predict(image, verbose=0)
    pred = raw_pred.argmax(axis=1)
    return hebrew_dict[pred[0]], raw_pred[0][pred[0]]

def update_prediction_label(prediction_label):
    # Get current frame from video capture
    ret, frame = cap.read()
    if ret:
        processed_frame = cut_image(frame, (128,128))
        prediction = predict_image(processed_frame)[0]
        prediction_label.config(text=prediction)
    else:
        prediction_label.config(text="Error: Could not capture frame")

### end of KERAS ML REGION

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


def q_append(a):
    try:
        lock_queue.acquire()
        prediction_queue.appendleft(a)
        lock_queue.release()
        return True
    except Exception:
        return False


def q_pop():
    popped = None
    try:
        lock_queue.acquire()
        popped = prediction_queue.pop()
        lock_queue.release()
        return popped
    except Exception:
        return False

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
logger.info(f"initialazing homePage")
### region Homepage
home_top_frame = tk.Frame(root, bg=BG_COLOR)
home_middle_frame = tk.Frame(root, bg=BG_COLOR)
home_bottom_frame = tk.Frame(root, bg=BG_COLOR)

logo_label = tk.Label(home_top_frame, image=logo_img, bg=BG_COLOR ) #bg=BG_COLOR
logo_label.pack(side='top', fill='x')


left_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)  
left_frame.pack(side="left")

left_button = tk.Button(left_frame, image=het_img, bg=BG_COLOR, borderwidth=0,
                        command=lambda: [start_camera(), show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
left_button.pack()
left_button_label = tk.Label(left_frame, text="בואו נלמד כיצד", bg=BG_COLOR, fg="black", font=("Calibri", 20))
left_button_label.pack(pady=0)

practice_label = tk.Label(left_frame, text="לכתוב את השם שלכם", bg=BG_COLOR, fg="black", font=("Calibri", 20))
practice_label.pack(pady=0)

boy_label = tk.Label(home_middle_frame, image=boy_img, bg=BG_COLOR)
boy_label.pack(side="left")

right_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=shin_img, bg=BG_COLOR, borderwidth=0, #bd=0, activebackground=BG_COLOR,
                         command=lambda: [start_camera(),show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
right_button.pack()
right_button_label = tk.Label(right_frame, text="בואו נתרגל", bg=BG_COLOR, fg="black", font=("Calibri", 20))
right_button_label.pack(pady=2)

practice_label = tk.Label(right_frame, text="אותיות ביחד", bg=BG_COLOR, fg="black", font=("Calibri", 20))
practice_label.pack(pady=0)


welcome_label = tk.Label(home_bottom_frame, text="!היי חברים, ברוכים הבאים", font=("Calibri", 34),  bg=BG_COLOR, fg="black") #bg=BG_COLOR
welcome_label.pack(side='left', padx=30)

######## build a word

build_a_word_button = tk.Button(home_bottom_frame, text = "בנה מילה", font=("Calibri", 34),  bg=BG_COLOR, fg="black",
                                 command= lambda:
                                   [start_camera(),
                                     show_build_a_word_frame(home_top_frame, home_middle_frame, home_bottom_frame)
                                     ])
build_a_word_button.pack(side='bottom', padx=30)

####### build a word




home_top_frame.pack(pady=10)
home_middle_frame.pack()
home_bottom_frame.pack(pady=10)

### end region homepage

video_label = tk.Label(root, bg=BG_COLOR)


### region idetify_page
logger.info(f"initialazing identify page")
# Create frames for the 'identify' layout
identify_top_frame = tk.Frame(root, bg=BG_COLOR)
identify_middle_frame = tk.Frame(root, bg=BG_COLOR)
identify_bottom_frame = tk.Frame(root, bg=BG_COLOR)

# Add widgets to the middle frame
identify_header = tk.Label(identify_top_frame, text="?תוכלו לעזור לי לגלות את אותיות שפת הסימנים", bg=BG_COLOR, font=("Calibri", 24))
identify_header.pack(pady=8)

identify_boy_label = tk.Label(identify_middle_frame, image=boy_img, bg=BG_COLOR)
identify_boy_label.pack(side="left")

prediction_frame = tk.Frame(identify_middle_frame, bg=BG_COLOR, padx=10, pady=5)
prediction_frame.pack(side="bottom", pady=0, padx=20)
prediction_label = tk.Label(prediction_frame, text="", bg=BG_COLOR, font=("Calibri", 20))
prediction_label.pack(side="left")
prediction_label_heder = tk.Label(prediction_frame, text=":הכירו את האות", bg=BG_COLOR, font=("Calibri", 20))
prediction_label_heder.pack(side='right', padx=50)

# Add widgets to the bottom frame
back_button = tk.Button(identify_bottom_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                        command=lambda: [close_camera(), show_home_frame(identify_middle_frame, identify_bottom_frame, video_label, identify_top_frame)])
back_button.pack(side="left", padx=0, pady=10)  

### end region identify_page


### region name_breakdown
logger.info(f"initialazing name breakdown page")
# Create frames for name_breakdown
name_breakdown_top_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_middle_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_bottom_frame = tk.Frame(root, bg=BG_COLOR)

# Add widgets to the top frame
name_breakdown_header = tk.Label(name_breakdown_top_frame, text="?מה השם שלך", font=("Calibri", 20),  bg=BG_COLOR, fg="black") #bg=BG_COLOR
name_breakdown_header.pack(side="top", padx=0)

submit_button = tk.Button(name_breakdown_top_frame, image=submit_img, bg=BG_COLOR, borderwidth=0,
                          highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                          command=lambda: break_down_name(name_entry.get(), letter_label, congrats_label))
submit_button.pack(side="left", padx=10)

name_entry = tk.Entry(name_breakdown_top_frame, font=("Calibri", 20), justify="right")
name_entry.pack(side="left", padx=10)

name_back_button = tk.Button(name_breakdown_top_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                             highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                             command=lambda: [close_camera(), show_home_frame(name_breakdown_top_frame, name_breakdown_middle_frame, name_breakdown_bottom_frame, video_label)])
name_back_button.pack(side="right", padx=10)



# Add widgets to the middle frame

next_button = tk.Button(name_breakdown_middle_frame, image=next_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                        command=lambda: display_next_letter(name_letters, letter_label, next_button, congrats_label))
next_button.pack_forget()  

congrats_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR, font=("Arial", 20))
congrats_label.pack(side="bottom", pady=0)

letter_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR)
letter_label.pack(side="left", padx=0)

# Function to break down the name into letters
def break_down_name(name, letter_label,  congrats_label):
    global name_letters, current_letter_index
    name_letters = list(name)
    if len(name_letters) <=0:
        return
    display_letter_image(name_letters[0], letter_label)
    congrats_label.config(text="")
    current_letter_index = 0
    # next_button.pack(side="left", padx=20)  # Move this line here

def check_prediction(letter_label, current_letter, ):
    flag = 0
    lock_prediction.acquire()
    try:
        if prediction == current_letter:
            next_button.pack(side="left", padx=20)  # Show the next_button
            flag = 1
            image = Image.open(r"letters\empty.png")
            image = ImageOps.exif_transpose(image)  
            image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
            letter_label.config(image=image)
        else:
            letter_label.config(fg="red")
    finally:
        lock_prediction.release()
    
    if flag:
        return
    root.after(100, check_prediction, letter_label, current_letter)

# Function to display the letter image
def display_letter_image(letter, label):
    if letter =='ן':
        letter = "נ"
    image_file = f"letters/{letter}.png"
    if os.path.exists(image_file):
        image = Image.open(image_file)
        image = ImageOps.exif_transpose(image)  # Rotate the image based on EXIF metadata
        image = ImageTk.PhotoImage(image.resize((300, 300), Image.LANCZOS))
        label.config(image=image, fg="black")  # Reset the foreground color
        label.image = image  # Keep a reference to prevent garbage collection
        root.after(100, check_prediction, label, letter)  # Start the prediction checking loop
    else:
        label.config(text=letter, image="")  # Clear the image reference

# Function to display the next letter
def display_next_letter(name_letters, letter_label, next_button, congrats_label):
    global current_letter_index
    try:
        next_button.pack_forget()  # Hide the next_button
        current_letter_index += 1
        if current_letter_index < len(name_letters):
            display_letter_image(name_letters[current_letter_index], letter_label)
            congrats_label.config(text="")
        else:
            congrats_label.config(text="!כל הכבוד")
    except Exception as e:
        print(f"Error: {e}")

### end region name_breakdown



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



def building_words():
    global prediction, prediction_queue, No_hands_flag
    prediction_queue = deque(maxlen=1000000)
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


### video Control region
logger.info(f"initialazing camera contol functions")
def start_camera():
    global cap, img_refs, camera_thread, keep_running, prediction_queue
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        img_refs = []
        keep_running = True
        logger.info("Camera is initialized!")
        camera_thread = threading.Thread(target=update_video, daemon=True)
        camera_thread.start()

def update_video():
    global cap, img_refs, keep_running, frame_counter, prediction, No_hands_flag
    counter_for_None_hands = 0
    No_hands_flag = 0
    while keep_running:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.config(image=img)
            if len(img_refs) > 10:
                img_refs.pop(0)
            img_refs.append(img)

            frame_counter += 1
            if frame_counter % 5 == 0:
                processed_frame = cut_image(frame, (128,128))
                if processed_frame is None:
                    counter_for_None_hands += 1
                else:
                    counter_for_None_hands = 0
                if counter_for_None_hands >= 30:
                    No_hands_flag = 1
                else:
                    No_hands_flag = 0
                
                lock_prediction.acquire()
                try:
                    prediction = predict_image(processed_frame)
                    if float(prediction[1]) > 0.60:
                        q_append(prediction[0])
                except Exception:
                    logger.critical("Reached exception in update_video()")
                    continue
                finally:
                    lock_prediction.release()
                if float(prediction[1]) > 0.68:
                    prediction_label.config(text=prediction[0])

        else:
            continue

def close_camera():
    global cap, keep_running
    keep_running = False
    if camera_thread and camera_thread.is_alive:
        cap.release()
        camera_thread.join(timeout=1)  # Wait for the camera thread to finish
        print("LOG: ", "releasing camera") # If thread is still alive, force terminate
           

### end video control region

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