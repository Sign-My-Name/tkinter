import tkinter as tk
from PIL import Image, ImageTk
import cv2
import random

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
left_button = tk.Button(left_frame, image=five_img, bg="#FEE4FC", borderwidth=0, command=lambda: show_identify_frame(top_frame, middle_frame, bottom_frame))
left_button.pack()
left_button_label = tk.Label(left_frame, text="Predict", bg="#FEE4FC", font=("Arial", 14))
left_button_label.pack(pady=5)

boy_label = tk.Label(middle_frame, image=boy_img, bg="#FEE4FC")
boy_label.pack(side="left")

right_frame = tk.Frame(middle_frame, bg="#FEE4FC")
right_frame.pack(side="left", padx=10)
right_button = tk.Button(right_frame, image=five_img, bg="#FEE4FC", borderwidth=0, command=lambda: show_identify_frame(top_frame, middle_frame, bottom_frame))
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
    prediction_label_heder = tk.Label(prediction_frame, text=":האות היא",bg="#FEE4FC", font=("Arial", 20) )
    prediction_label_heder.pack(side='left')
  

    # Add widgets to the bottom frame
    back_button = tk.Button(identify_bottom_frame, image=back_img, bg="#FEE4FC", borderwidth=0, highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0, command=lambda: show_home_frame(top_frame, middle_frame, bottom_frame, identify_middle_frame, identify_bottom_frame, video_label))
    back_button.pack(side="left", padx=0, pady=10)  # Moved 200 pixels to the left

    predict_button = tk.Button(identify_bottom_frame, image=predict_img, bg="#FEE4FC", borderwidth=0, highlightbackground="#FEE4FC", highlightcolor="#FEE4FC", highlightthickness=0, command=lambda: update_prediction_label(prediction_label))
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
    hebrew_letters = 'אבגדהוזחטיכלמנסעפצקרשת'
    random_letter = random.choice(hebrew_letters)
    prediction_label.config(text=random_letter)

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