import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import tensorflow as tf
import os
import threading


# Create the main window
root = tk.Tk()
root.title("SignMyName")
root.configure(bg="#FEE4FC")  # Set the background color
root.minsize(1200, 720)  # Set the minimum window size



cap = None
camera_thread = None
keep_running = False

# Load images
logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((418, 200), Image.LANCZOS))
boy_img = ImageTk.PhotoImage(Image.open("assets/boy.png").resize((350, 350), Image.LANCZOS))
five_img = ImageTk.PhotoImage(Image.open("assets/five.png").resize((150, 145), Image.LANCZOS))
back_img = ImageTk.PhotoImage(Image.open("assets/back.png").resize((124, 67), Image.LANCZOS))
predict_img = ImageTk.PhotoImage(Image.open("assets/predict.png").resize((174, 68), Image.LANCZOS))
submit_img = ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS))
next_img = ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS))


# Create frames for the grid layout for home_page
### region Homepage
home_top_frame = tk.Frame(root, bg="#FEE4FC")
home_middle_frame = tk.Frame(root, bg="#FEE4FC")
home_bottom_frame = tk.Frame(root, bg="#FEE4FC")

logo_label = tk.Label(home_top_frame, image=logo_img, bg="#FEE4FC")
logo_label.pack(side='left')

left_frame = tk.Frame(home_middle_frame, bg="#FEE4FC")
left_frame.pack(side="left", padx=10)
left_button = tk.Button(left_frame, image=five_img, bg="#FEE4FC", borderwidth=0,
                        command=lambda: [start_camera(), show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
left_button.pack()
left_button_label = tk.Label(left_frame, text="Predict", bg="#FEE4FC", font=("Arial", 14))
left_button_label.pack(pady=5)

boy_label = tk.Label(home_middle_frame, image=boy_img, bg="#FEE4FC")
boy_label.pack(side="left")

right_frame = tk.Frame(home_middle_frame, bg="#FEE4FC")
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=five_img, bg="#FEE4FC", borderwidth=0,
                         command=lambda: [start_camera(),show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame)])
right_button.pack()
right_button_label = tk.Label(right_frame, text="Identify", bg="#FEE4FC", font=("Arial", 14))
right_button_label.pack(pady=5)


home_top_frame.pack(pady=10)
home_middle_frame.pack()
home_bottom_frame.pack(pady=10)



video_label = tk.Label(root, bg="#FEE4FC")






### end region homepage

### region idetify_page
# Create frames for the 'identify' layout
identify_middle_frame = tk.Frame(root, bg="#FEE4FC")
identify_bottom_frame = tk.Frame(root, bg="#FEE4FC")

# Add widgets to the middle frame


identify_boy_label = tk.Label(identify_middle_frame, image=boy_img, bg="#FEE4FC")
identify_boy_label.pack(side="left")

prediction_frame = tk.Frame(identify_middle_frame, bg="#FEE4FC", padx=10, pady=5)
prediction_frame.pack(side="bottom", pady=10, padx=20)
prediction_label = tk.Label(prediction_frame, text="", bg="#FEE4FC", font=("Arial", 20))
prediction_label.pack(side="left")
prediction_label_heder = tk.Label(prediction_frame, text=":האות היא", bg="#FEE4FC", font=("Arial", 20))
prediction_label_heder.pack(side='left')

# Add widgets to the bottom frame
back_button = tk.Button(identify_bottom_frame, image=back_img, bg="#FEE4FC", borderwidth=0,
                        highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                        command=lambda: [close_camera(), show_home_frame(identify_middle_frame, identify_bottom_frame, video_label)])
back_button.pack(side="left", padx=0, pady=10)  

predict_button = tk.Button(identify_bottom_frame, image=predict_img, bg="#FEE4FC", borderwidth=0,
                            highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                            command=lambda: update_prediction_label(prediction_label))
predict_button.pack(side="left", padx=0, pady=10)

### end region identify_page



### region name_breakdown
# Create frames for name_breakdown
name_breakdown_top_frame = tk.Frame(root, bg="#FEE4FC")
name_breakdown_middle_frame = tk.Frame(root, bg="#FEE4FC")
name_breakdown_bottom_frame = tk.Frame(root, bg="#FEE4FC")

# Add widgets to the top frame
name_entry = tk.Entry(name_breakdown_top_frame, font=("Arial", 20))
name_entry.pack(side="left", padx=10)

name_back_button = tk.Button(name_breakdown_top_frame, image=back_img, bg="#FEE4FC", borderwidth=0,
                             highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                             command=lambda: [close_camera(), show_home_frame(name_breakdown_top_frame, name_breakdown_middle_frame, name_breakdown_bottom_frame, video_label)])
name_back_button.pack(side="left", padx=10)

submit_button = tk.Button(name_breakdown_top_frame, image=submit_img, bg="#FEE4FC", borderwidth=0,
                          highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                          command=lambda: break_down_name(name_entry.get(), letter_label, name_label, congrats_label))
submit_button.pack(side="left", padx=10)

# Add widgets to the middle frame
name_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC", font=("Arial", 20))
name_label.pack(side="top", pady=10)

letter_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC", font=("Arial", 100))
letter_label.pack(side="left", padx=20)

next_button = tk.Button(name_breakdown_middle_frame, image=next_img, bg="#FEE4FC", borderwidth=0,
                        highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                        command=lambda: display_next_letter(name_letters, letter_label, next_button, congrats_label))

congrats_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC", font=("Arial", 20))
congrats_label.pack(side="bottom", pady=10)

video_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC")
video_label.pack(pady=10, fill='both', expand='true')

# Function to break down the name into letters
def break_down_name(name, letter_label, name_label, congrats_label):
    global name_letters
    name_letters = list(name)
    name_label.config(text=f"Name: {name}")
    letter_label.config(text=name_letters[0])
    congrats_label.config(text="")
    next_button.pack(side="left", padx=10)

# Function to display the next letter
def display_next_letter(name_letters, letter_label, next_button, congrats_label):
    try:
        current_letter_index = name_letters.index(letter_label.cget("text"))
        next_letter_index = current_letter_index + 1
        letter_label.config(text=name_letters[next_letter_index])
        congrats_label.config(text="")
        if next_letter_index == len(name_letters) - 1:
            next_button.pack_forget()
            congrats_label.config(text="Congratulations!")
    except ValueError:
        pass

### end region name_breakdown



### video Control region
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
    global cap, img_refs, keep_running
    while keep_running:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.config(image=img)
            if len(img_refs) > 10:
                img_refs.pop(0)
            img_refs.append(img)
        else:
            continue
    
def close_camera():
    global cap, keep_running
    keep_running = False
    if camera_thread and camera_thread.is_alive:
        cap.release()
        camera_thread.join(timeout=1)  # Wait for the camera thread to finish
        print("LOG: ", "Triying to release camera") # If thread is still alive, force terminate
           

### end video control region

### frame contol region

def show_identify_frame(home_top_frame, home_middle_frame, home_bottom_frame):
    global video_label
    video_label.pack_forget()

    home_top_frame.pack_forget()
    home_middle_frame.pack_forget()
    home_bottom_frame.pack_forget()


    video_label = tk.Label(identify_middle_frame, bg="#FEE4FC")

    identify_middle_frame.pack(pady=10)
    identify_bottom_frame.pack(pady=10)
    video_label.pack(side="right", padx=10)



def show_name_breakdown_frame(home_top_frame, home_middle_frame, home_bottom_frame):
    global video_label
    video_label.pack_forget()

    home_top_frame.pack_forget()
    home_middle_frame.pack_forget()
    home_bottom_frame.pack_forget()

    video_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC")

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

root.mainloop()