import tkinter as tk
from PIL import Image, ImageTk 
import cv2
import threading

root = tk.Tk()
root.minsize(1200, 720)
root.title("test")

# Label1 = tk.Label(root, bg='red', image=)
# Label1.pack(expand=True, fill='both')

# placeholder_img = ImageTk.PhotoImage(Image.open("placeholder.png").resize((640, 480), Image.LANCZOS))
videoLabel = tk.Label(root, bg='yellow')
videoLabel.pack(pady=10, fill='both', expand='True')


def testbutton():
    print(f'i was pressed')

button = tk.Button(root, text="Im here as a test", command=lambda:[testbutton()])
button.pack()
# predictionLabel = tk.Label(mainFrame, text='', bg='pink2', font=("Calibri", 80, 'bold'))
# predictionLabel.pack()

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
    # videorun()

def update_video():
    global cap
    # while True:
    ret, frame = cap.read()
    # while True:
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        videoLabel.configure(image=img)
        videoLabel.image = img
    root.after(1, update_video)



# def videorun():
#     global cap
#     _, frame = cap.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     img = ImageTk.PhotoImage(image=Image.fromarray(frame))
#     videoLabel.configure(image=img)
#     root.after(10,videorun)


start_camera()
root.mainloop()