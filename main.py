import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info(f"initializing imports: cv2, numpy, tkinter, PIL")
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
logger.info(f"initializing imports: mediapipe")
import mediapipe as mp
logger.info(f"initializing imports: tensorflow")
import tensorflow as tf
logger.info(f"initializing imports: os, threading")
import os
import threading

### KERAS ML RESGION
logger.info(f"initializing tensorflow's keras and model loading")
# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load the trained model
loaded_model_dir = r'ML/model/model.h5'
loaded_model = tf.keras.models.load_model(loaded_model_dir)
class_to_letter = ['B', 'C', 'D', 'F', 'I', 'L', 'M', 'N', 'R', 'S', 'T', 'W', 'Z', 'nothing']
english_to_hebrew = {
    'B': 'ב', 'C': 'כ', 'D': 'ו', 'F': 'ט', 'I': 'י', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'R': 'ר', 'S': 'ס',
    'T': 'ת', 'W': 'ש', 'Z': 'ז'
}

# Initialize the MediaPipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def cut_image(image, size=(128, 128)):
    image = image.astype(np.uint8)
    processed_image = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if processed_image.multi_hand_landmarks:
        hand_landmarks = processed_image.multi_hand_landmarks[0]
        x_coords = [landmark.x for landmark in hand_landmarks.landmark]
        y_coords = [landmark.y for landmark in hand_landmarks.landmark]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        x_min_adjust = int(x_min * image.shape[1] - 80)
        y_min_adjust = int(y_min * image.shape[0] - 80)
        x_max_adjust = int(x_max * image.shape[1] + 80)
        y_max_adjust = int(y_max * image.shape[0] + 80)
        x_min_adjust = max(int(x_min * image.shape[1] - 15), 0)
        y_min_adjust = max(int(y_min * image.shape[0] - 15), 0)

        image = image[y_min_adjust:y_max_adjust, x_min_adjust:x_max_adjust]
        hand_region_uint8 = image.astype(np.uint8)
        hand_region_bgr = cv2.cvtColor(hand_region_uint8, cv2.COLOR_RGB2BGR)
        hand_region_bgr = cv2.resize(hand_region_bgr, dsize=size)
    else:
        hand_region_bgr = None
    return hand_region_bgr

def predict_image(image):
    if image is None:
        return ""
    # Make a prediction on the single image
    image = np.expand_dims(image, axis=0)
    raw_pred = loaded_model.predict(image)
    pred = raw_pred.argmax(axis=1)
    print(class_to_letter[pred[0]])
    return english_to_hebrew[class_to_letter[pred[0]]]

def update_prediction_label(prediction_label):
    # Get current frame from video capture
    ret, frame = cap.read()
    if ret:
        processed_frame = cut_image(frame)
        prediction = predict_image(processed_frame)
        prediction_label.config(text=prediction)
    else:
        prediction_label.config(text="Error: Could not capture frame")

### end of KERAS ML REGION

BG_COLOR = "#FEE4FC"


logger.info(f"initializing tkinter")
# Create the main window
root = tk.Tk()
root.title("SignMyName")
root.configure(bg=BG_COLOR)  # Set the background color
root.minsize(1200, 720)  # Set the minimum window size

logger.info(f"initialazing lock")
lock = threading.Lock()

logger.info(f"initialazing global vars")
cap = None
camera_thread = None
keep_running = False
frame_counter = 0
prediction = ""



# Load images
logger.info(f"initialazing images")
logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((418, 200), Image.LANCZOS))
boy_img = ImageTk.PhotoImage(Image.open("assets/boy.png").resize((350, 350), Image.LANCZOS))
five_img = ImageTk.PhotoImage(Image.open("assets/five.png").resize((150, 145), Image.LANCZOS))
back_img = ImageTk.PhotoImage(Image.open("assets/back.png").resize((124, 67), Image.LANCZOS))
predict_img = ImageTk.PhotoImage(Image.open("assets/predict.png").resize((174, 68), Image.LANCZOS))
submit_img = ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS))
next_img = ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS))


# Create frames for the grid layout for home_page
logger.info(f"initialazing homePage")
### region Homepage
home_top_frame = tk.Frame(root, bg=BG_COLOR)
home_middle_frame = tk.Frame(root, bg=BG_COLOR)
home_bottom_frame = tk.Frame(root, bg=BG_COLOR)

logo_label = tk.Label(home_top_frame, image=logo_img, bg=BG_COLOR)
logo_label.pack(side='left')

left_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)
left_frame.pack(side="left", padx=10)
left_button = tk.Button(left_frame, image=five_img, bg=BG_COLOR, borderwidth=0,
                        command=lambda: [start_camera(), show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
left_button.pack()
left_button_label = tk.Label(left_frame, text="Predict", bg=BG_COLOR, font=("Arial", 14))
left_button_label.pack(pady=5)

boy_label = tk.Label(home_middle_frame, image=boy_img, bg=BG_COLOR)
boy_label.pack(side="left")

right_frame = tk.Frame(home_middle_frame, bg=BG_COLOR)
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=five_img, bg=BG_COLOR, borderwidth=0,
                         command=lambda: [start_camera(),show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
right_button.pack()
right_button_label = tk.Label(right_frame, text="Identify", bg=BG_COLOR, font=("Arial", 14))
right_button_label.pack(pady=5)


home_top_frame.pack(pady=10)
home_middle_frame.pack()
home_bottom_frame.pack(pady=10)

### end region homepage


video_label = tk.Label(root, bg=BG_COLOR)


### region idetify_page
logger.info(f"initialazing identify page")
# Create frames for the 'identify' layout
identify_middle_frame = tk.Frame(root, bg=BG_COLOR)
identify_bottom_frame = tk.Frame(root, bg=BG_COLOR)

# Add widgets to the middle frame


identify_boy_label = tk.Label(identify_middle_frame, image=boy_img, bg=BG_COLOR)
identify_boy_label.pack(side="left")

prediction_frame = tk.Frame(identify_middle_frame, bg=BG_COLOR, padx=10, pady=5)
prediction_frame.pack(side="bottom", pady=10, padx=20)
prediction_label = tk.Label(prediction_frame, text="", bg=BG_COLOR, font=("Arial", 20))
prediction_label.pack(side="left")
prediction_label_heder = tk.Label(prediction_frame, text=":האות היא", bg=BG_COLOR, font=("Arial", 20))
prediction_label_heder.pack(side='left')

# Add widgets to the bottom frame
back_button = tk.Button(identify_bottom_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                        command=lambda: [close_camera(), show_home_frame(identify_middle_frame, identify_bottom_frame, video_label)])
back_button.pack(side="left", padx=0, pady=10)  

predict_button = tk.Button(identify_bottom_frame, image=predict_img, bg=BG_COLOR, borderwidth=0,
                            highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                            command=lambda: update_prediction_label(prediction_label))
predict_button.pack(side="left", padx=0, pady=10)

### end region identify_page



### region name_breakdown
logger.info(f"initialazing name breakdown page")
# Create frames for name_breakdown
name_breakdown_top_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_middle_frame = tk.Frame(root, bg=BG_COLOR)
name_breakdown_bottom_frame = tk.Frame(root, bg=BG_COLOR)

# Add widgets to the top frame
name_entry = tk.Entry(name_breakdown_top_frame, font=("Arial", 20))
name_entry.pack(side="left", padx=10)

name_back_button = tk.Button(name_breakdown_top_frame, image=back_img, bg=BG_COLOR, borderwidth=0,
                             highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                             command=lambda: [close_camera(), show_home_frame(name_breakdown_top_frame, name_breakdown_middle_frame, name_breakdown_bottom_frame, video_label)])
name_back_button.pack(side="left", padx=10)

submit_button = tk.Button(name_breakdown_top_frame, image=submit_img, bg=BG_COLOR, borderwidth=0,
                          highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                          command=lambda: break_down_name(name_entry.get(), letter_label, name_label, congrats_label))
submit_button.pack(side="left", padx=10)

# Add widgets to the middle frame
name_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR, font=("Arial", 20))
name_label.pack(side="top", pady=10)

letter_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR)
letter_label.pack(side="left", padx=20)

next_button = tk.Button(name_breakdown_middle_frame, image=next_img, bg=BG_COLOR, borderwidth=0,
                        highlightbackground=BG_COLOR, highlightcolor=BG_COLOR, highlightthickness=0,
                        command=lambda: display_next_letter(name_letters, letter_label, next_button, congrats_label))
next_button.pack_forget()  

congrats_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR, font=("Arial", 20))
congrats_label.pack(side="bottom", pady=10)

video_label = tk.Label(name_breakdown_middle_frame, bg=BG_COLOR)
video_label.pack(pady=50, fill='both', expand='true')

# Function to break down the name into letters
def break_down_name(name, letter_label, name_label, congrats_label):
    global name_letters, current_letter_index
    name_letters = list(name)
    name_label.config(text=f":שם {name}")
    if len(name_letters) <=0:
        return
    display_letter_image(name_letters[0], letter_label)
    congrats_label.config(text="")
    current_letter_index = 0
    # next_button.pack(side="left", padx=20)  # Move this line here


def check_prediction(letter_label, current_letter, ):
    flag = 0
    lock.acquire()
    logger.info("LOG:", "prediction: ", prediction, "current letter: ", current_letter)
    try:
        if prediction == current_letter:
            next_button.pack(side="left", padx=20)  # Show the next_button
            flag = 1
            letter_label.config(image="")
        else:
            letter_label.config(fg="red")
    finally:
        lock.release()
    
    if flag:
        return
    root.after(100, check_prediction, letter_label, current_letter)

# Function to display the letter image
def display_letter_image(letter, label):
    image_file = f"letters/{letter}.jpg"
    if os.path.exists(image_file):
        image = Image.open(image_file)
        image = ImageOps.exif_transpose(image)  # Rotate the image based on EXIF metadata
        image = ImageTk.PhotoImage(image.resize((200, 300), Image.LANCZOS))
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
            congrats_label.config(text="Congratulations!")
    except Exception as e:
        print(f"Error: {e}")

### end region name_breakdown

### video Control region
logger.info(f"initialazing camera contol functions")
def start_camera():
    global cap, img_refs, camera_thread, keep_running
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        img_refs = []
        keep_running = True
        print("LOG: ", "Camera is initialized!")
        camera_thread = threading.Thread(target=update_video, daemon=True)
        camera_thread.start()

def update_video():
    global cap, img_refs, keep_running, frame_counter, prediction
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
                processed_frame = cut_image(frame)
                lock.acquire()
                try:
                    prediction = predict_image(processed_frame)
                finally:
                    lock.release()
                prediction_label.config(text=prediction)

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


def show_home_frame(middle_frame, bottom_frame, video_label, top_frame=None):
    if top_frame:
        top_frame.pack_forget()
    middle_frame.pack_forget()
    bottom_frame.pack_forget()
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