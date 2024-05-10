import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import threading




root = tk.Tk()
root.minsize(1200, 720)
root.title("test")



label1 = tk.Label(root, text="Test", bg='red')
label1.pack(side='left', expand=True, fill='both')

mainFrame = tk.Frame(root, bg='blue')
mainFrame.pack(expand=True, fill='both')

placeholder_img = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640, 480), Image.LANCZOS))
videoLabel = tk.Label(mainFrame, image=placeholder_img, bg='yellow')
videoLabel.pack(fill='y', expand=True)

predictionLabel = tk.Label(mainFrame, text='', bg='pink2', font=("Calibri", 80, 'bold'))
predictionLabel.pack()

# cap = proj_camera()

# cap.start_camera(videoLabel, predictionLabel, None)
cap = None
def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera_thread = threading.Thread(target=update_video, daemon=True)
    camera_thread.start()

def update_video():
    global cap, videoLabel
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            videoLabel.config(image=img)


start_camera()
root.mainloop()