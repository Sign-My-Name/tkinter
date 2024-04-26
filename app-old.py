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
loaded_model_dir = r'asl_new_NoWeights_bs=32_ts=(128, 128)_valSplit=0.2_lr=0.001_epochs=120.h5'
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
                        command=lambda: show_name_breakdown_frame(top_frame, middle_frame, bottom_frame))
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



def show_name_breakdown_frame(top_frame, middle_frame, bottom_frame):
    # Hide the home screen frames
    top_frame.pack_forget()
    middle_frame.pack_forget()
    bottom_frame.pack_forget()

    # Create frames for the 'name breakdown' layout
    name_breakdown_middle_frame = tk.Frame(root, bg="#FEE4FC")
    name_breakdown_bottom_frame = tk.Frame(root, bg="#FEE4FC")

    # Add widgets to the middle frame
    name_entry = tk.Entry(name_breakdown_middle_frame, font=("Arial", 20))
    name_entry.pack(pady=20)

    letter_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC", font=("Arial", 100))
    letter_label.pack(side="left", padx=20)

    video_label = tk.Label(name_breakdown_middle_frame, bg="#FEE4FC")
    video_label.pack(side="left", padx=20)

    # Add widgets to the bottom frame
    back_button = tk.Button(name_breakdown_bottom_frame, image=back_img, bg="#FEE4FC", borderwidth=0,
                            highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0,
                            command=lambda: show_home_frame(top_frame, middle_frame, bottom_frame,
                                                            name_breakdown_middle_frame, name_breakdown_bottom_frame,
                                                            video_label))
    back_button.pack(side="left", padx=10, pady=10)

    # Add frames to the root window
    name_breakdown_middle_frame.pack(pady=10)
    name_breakdown_bottom_frame.pack(pady=10)

    def start_name_breakdown(name):
        show_name_breakdown_frame.target_letters = [letter.lower() for letter in name]
        show_name_breakdown_frame.current_letter_index = 0
        show_name_breakdown_frame.letter_images = [ImageTk.PhotoImage(Image.open(f"letters/{letter}.jpg").resize((100, 100), Image.LANCZOS)) for letter in show_name_breakdown_frame.target_letters]
        letter_label.configure(image=show_name_breakdown_frame.letter_images[0])

        # Cancel any existing update_video_and_prediction loop
        if hasattr(show_home_frame, 'update_video_and_prediction_after_id'):
            root.after_cancel(show_home_frame.update_video_and_prediction_after_id)
            del show_home_frame.update_video_and_prediction_after_id

        # Start the update_video_and_prediction loop
        update_video_and_prediction()
        show_home_frame.update_video_and_prediction_after_id = update_video_and_prediction.after_id



    def update_video_and_prediction():
        ret, frame = cap.read()
        if ret:
            # Process every 5th frame
            if update_video_and_prediction.frame_count % 5 == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                video_label.configure(image=img)
                video_label.image = img

                # Get hand region and make prediction
                hand_region = cut_image(frame)
                predicted_letter = predict_image(hand_region)

                # Check if predicted letter matches the current target letter
                if show_name_breakdown_frame.current_letter_index < len(show_name_breakdown_frame.target_letters):
                    if predicted_letter == show_name_breakdown_frame.target_letters[show_name_breakdown_frame.current_letter_index]:
                        show_name_breakdown_frame.current_letter_index += 1
                        if show_name_breakdown_frame.current_letter_index >= len(show_name_breakdown_frame.target_letters):
                            letter_label.configure(text="Congratulations!")
                            # Stop the update_video_and_prediction loop
                            root.after_cancel(update_video_and_prediction.after_id)
                            del update_video_and_prediction.after_id
                        else:
                            letter_label.configure(image=show_name_breakdown_frame.letter_images[show_name_breakdown_frame.current_letter_index])
                else:
                    # All letters have been recognized, stop the loop
                    root.after_cancel(update_video_and_prediction.after_id)
                    del update_video_and_prediction.after_id
                    letter_label.configure(text="Congratulations!")

            update_video_and_prediction.frame_count += 1
        update_video_and_prediction.after_id = root.after(10, update_video_and_prediction)

    update_video_and_prediction.frame_count = 0

    def start_name_breakdown(name):
        show_name_breakdown_frame.target_letters = [letter.lower() for letter in name]
        show_name_breakdown_frame.current_letter_index = 0
        show_name_breakdown_frame.letter_images = [ImageTk.PhotoImage(Image.open(f"letters/{letter}.jpg").resize((100, 100), Image.LANCZOS)) for letter in show_name_breakdown_frame.target_letters]
        letter_label.configure(image=show_name_breakdown_frame.letter_images[0])
        update_video_and_prediction()

    submit_button = tk.Button(name_breakdown_middle_frame, text="Submit", bg="#FEE4FC", font=("Arial", 14),
                              command=lambda: start_name_breakdown(name_entry.get()))
    submit_button.pack(side="right", padx=20)


    
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
def show_home_frame(top_frame, middle_frame, bottom_frame, name_breakdown_middle_frame, name_breakdown_bottom_frame, video_label):
    name_breakdown_middle_frame.pack_forget()
    name_breakdown_bottom_frame.pack_forget()
    video_label.pack_forget()  # Stop updating the video frame
    top_frame.pack(pady=10)
    middle_frame.pack()
    bottom_frame.pack(pady=10)

    # Stop the update_video_and_prediction loop
    if hasattr(show_home_frame, 'update_video_and_prediction_after_id'):
        root.after_cancel(show_home_frame.update_video_and_prediction_after_id)
        del show_home_frame.update_video_and_prediction_after_id

# Run the main loop
root.mainloop()