import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import tensorflow as tf
import os

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load the trained model
loaded_model_dir = r'C:\Users\40gil\Desktop\degree\year_4\sm2\final_project\running_outputs\asl_new_NoWeights_bs=32_ts=(128, 128)_valSplit=0.2_lr=0.001_epochs=120_DateTime=03_03_35\asl_new_NoWeights_bs=32_ts=(128, 128)_valSplit=0.2_lr=0.001_epochs=120.h5'
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
        if x_min_adjust < 0:
            x_min_adjust = int(x_min * image.shape[1] - 15)
            if x_min_adjust < 0:
                x_min_adjust = 0
        if y_min_adjust < 0:
            y_min_adjust = int(y_min * image.shape[0] - 15)
            if y_min_adjust < 0:
                y_min_adjust = 0
        x_min = x_min_adjust
        y_min = y_min_adjust
        x_max = x_max_adjust
        y_max = y_max_adjust
        hand_region = image[y_min:y_max, x_min:x_max]
        hand_region_uint8 = hand_region.astype(np.uint8)
    else:
        hand_region_uint8 = image.astype(np.uint8)
    hand_region_bgr = cv2.cvtColor(hand_region_uint8, cv2.COLOR_RGB2BGR)
    hand_region_bgr = cv2.resize(hand_region_bgr, dsize=size)
    return hand_region_bgr


def predict_image(image):
    if image is None:
        return "No image provided"
    # Make a prediction on the single image
    image = np.expand_dims(image, axis=0)
    raw_pred = loaded_model.predict(image)
    pred = raw_pred.argmax(axis=1)
    print(class_to_letter[pred[0]])
    return english_to_hebrew[class_to_letter[pred[0]]]

# Create the main window
root = tk.Tk()
root.title("SignMyName")
root.configure(bg="#FEE4FC")  # Set the background color
root.minsize(1200, 720)  # Set the minimum window size

# Load images
logo_img = ImageTk.PhotoImage(Image.open("logo.png").resize((418, 200), Image.LANCZOS))
boy_img = ImageTk.PhotoImage(Image.open("boy.png").resize((350, 350), Image.LANCZOS))
five_img = ImageTk.PhotoImage(Image.open("five.png").resize((150, 145), Image.LANCZOS))
back_img = ImageTk.PhotoImage(Image.open("back.png").resize((124, 67), Image.LANCZOS))
predict_img = ImageTk.PhotoImage(Image.open("predict.png").resize((174, 68), Image.LANCZOS))

# Create frames for the grid layout
top_frame = tk.Frame(root, bg="#FEE4FC")
middle_frame = tk.Frame(root, bg="#FEE4FC")
bottom_frame = tk.Frame(root, bg="#FEE4FC")

# Add widgets to the top frame
logo_label = tk.Label(top_frame, image=logo_img, bg="#FEE4FC")
logo_label.pack()

# Add widgets to the middle frame
left_frame = tk.Frame(middle_frame, bg="#FEE4FC")
left_frame.pack(side="left", padx=10)
left_button = tk.Button(left_frame, image=five_img, bg="#FEE4FC", borderwidth=0,
                        command=lambda: show_identify_frame(top_frame, middle_frame, bottom_frame))
left_button.pack()
left_button_label = tk.Label(left_frame, text="Predict", bg="#FEE4FC", font=("Arial", 14))
left_button_label.pack(pady=5)

boy_label = tk.Label(middle_frame, image=boy_img, bg="#FEE4FC")
boy_label.pack(side="left")

right_frame = tk.Frame(middle_frame, bg="#FEE4FC")
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=five_img, bg="#FEE4FC", borderwidth=0,
                         command=lambda: show_identify_frame(top_frame, middle_frame, bottom_frame))
right_button.pack()
right_button_label = tk.Label(right_frame, text="Identify", bg="#FEE4FC", font=("Arial", 14))
right_button_label.pack(pady=5)

# Add frames to the root window
top_frame.pack(pady=10)
middle_frame.pack()
bottom_frame.pack(pady=10)

# Start the video stream (replace this with your OpenCV code)
cap = cv2.VideoCapture(0)


# Function to show the 'identify' frame
def show_identify_frame(top_frame, middle_frame, bottom_frame):
    # Hide the home screen frames
    top_frame.pack_forget()
    middle_frame.pack_forget()
    bottom_frame.pack_forget()

    # Create frames for the 'identify' layout
    identify_middle_frame = tk.Frame(root, bg="#FEE4FC")
    identify_bottom_frame = tk.Frame(root, bg="#FEE4FC")

    # Add widgets to the middle frame
    video_label = tk.Label(identify_middle_frame, bg="#FEE4FC")
    video_label.pack(side="left", padx=10)

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
                            command=lambda: show_home_frame(top_frame, middle_frame, bottom_frame,
                                                            identify_middle_frame, identify_bottom_frame, video_label))
    back_button.pack(side="left", padx=0, pady=10)  # Moved 200 pixels to the left

    predict_button = tk.Button(identify_bottom_frame, image=predict_img, bg="#FEE4FC", borderwidth=0,
                               highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                               command=lambda: update_prediction_label(prediction_label))
    predict_button.pack(side="left", padx=0, pady=10)

    # Add frames to the root window
    identify_middle_frame.pack(pady=10)
    identify_bottom_frame.pack(pady=10)

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.config(image=img)
            video_label.image = img
        root.after(10, update_video)

    update_video()


# Function to update the prediction label with a random Hebrew letter
def update_prediction_label(prediction_label):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand region and make prediction
    hand_region = cut_image(frame)
    predicted_letter = predict_image(hand_region)

    # Display prediction

    # Update the video feed label
    # img = Image.fromarray(hand_region)
    # img = ImageTk.PhotoImage(image=img)
    prediction_label.config(text=predicted_letter)


# Function to show the home frame
def show_home_frame(top_frame, middle_frame, bottom_frame, identify_middle_frame, identify_bottom_frame, video_label):
    identify_middle_frame.pack_forget()
    identify_bottom_frame.pack_forget()
    video_label.pack_forget()  # Stop updating the video frame
    top_frame.pack(pady=10)
    middle_frame.pack()
    bottom_frame.pack(pady=10)

# Run the main loop
root.mainloop()