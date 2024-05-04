from proj_logger import get_logger

import os
import json
import requests
import subprocess
import tkinter as tk
from tkinter import ttk
import tensorflow as tf
import threading
import numpy as np

HEBREW_DICT = {
    0: 'א', 1: 'ב', 2: 'ג', 3: 'ד', 4: 'ה', 5: 'ו', 6: 'ז', 7: 'ח', 8: 'ט', 9: 'י', 10: 'כ', 11: 'ל', 12: 'מ', 13: 'נ',  
    14: 'ס', 15: 'ע', 16: 'פ', 17: 'צ', 18: 'ק', 19: 'ר', 20: 'ש', 21: 'ת'
}

# def update_prediction_label(cap, prediction_label):
#     # Get current frame from video capture
#     ret, frame = cap.read()
#     if ret:
#         processed_frame = cut_image(frame, (128,128))
#         prediction = predict_image(processed_frame)[0]
#         prediction_label.config(text=prediction)
#     else:
#         prediction_label.config(text="Error: Could not capture frame")

class predictor:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        self.logger =  get_logger()
        self.logger.info(f'init Predictor')
        self.model_repo_path = '\SignMyNameSivan\model'
        self.logger.info(f'start check for updates')
        self.loaded_model = self.check_for_updates()
    
    def predict_image(self, image):
        if image is None:
            return "",0.0
        # Make a prediction on the single image
        image = np.expand_dims(image, axis=0)
        raw_pred = self.loaded_model.predict(image, verbose=0)
        pred = raw_pred.argmax(axis=1)
        return HEBREW_DICT[pred[0]], raw_pred[0][pred[0]]

    def init_local_commit_hash(self):
        with open('conf.json', 'r') as file:
            config = json.load(file)
            self.local_commit_hash = config['model_commit_hash']

    def get_latest_commit_hash(self):
        # Setup the API URL to fetch the latest commit from the main branch
        api_url = 'https://api.github.com/repos/Sign-My-Name/Model/commits/main'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        # Make the API request
        try:
            response = requests.get(api_url, headers=headers)
        except Exception:
            self.logger.info("No connection to Git API, continueing")
            return None
        if response.status_code == 200:
            data = response.json()
            return data['sha']
        else:
            print("Failed to fetch commit data")
            return None

    def update_commit_hash_in_config(self, latest_commit_hash):
        # Load the existing data from the file
        with open('conf.json', 'r') as file:
            config = json.load(file)
        
        # Update the commit hash
        config['model_commit_hash'] = latest_commit_hash
        
        # Write the updated data back to the file
        with open('conf.json', 'w') as file:
            json.dump(config, file, indent=4)

    def update_model(self):
        try:
            os.makedirs(self.model_repo_path, exist_ok=True)
            if not os.path.exists(os.path.join(self.model_repo_path, '.git')):
                subprocess.run(['git', 'init'], cwd=self.model_repo_path, check=True)
                remote_repo_url = 'https://github.com/Sign-My-Name/Model.git'
                subprocess.run(['git', 'remote', 'add', 'origin', remote_repo_url], cwd=self.model_repo_path, check=True)
            
            subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.model_repo_path, check=True)
            self.logger.info("Model updated to the latest version.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to update the model: {e}")
        finally:
            return True

    def messageWindow(self):
        message_root = tk.Tk()
        message_root.withdraw()
        win = tk.Toplevel(message_root)
        win.title('יש עדכון')

        message = "?קיים עדכון למערכת, תרצה לעדכן"
        tk.Label(win, text=message).pack(pady=20)

        response = tk.BooleanVar(value=None)

        def yes_action():
            response.set(True)
            win.destroy()
            message_root.quit()

        def no_action():
            response.set(False)
            win.destroy()
            message_root.quit()

        button_frame = tk.Frame(win)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text='כן', command=yes_action).pack(side=tk.LEFT, padx=50)
        tk.Button(button_frame, text='לא', command=no_action).pack(side=tk.RIGHT, padx=50)

        message_root.wait_window(win)
        result = response.get()
        message_root.destroy()
        return result

    def check_for_updates(self):
        self.init_local_commit_hash()
        latest_commit_hash = self.get_latest_commit_hash()

        self.logger.info(f'checks for different hashes')

        if latest_commit_hash and self.local_commit_hash != latest_commit_hash:
            self.logger.info(f'start messageWindow')
            if self.messageWindow():
                self.logger.info(f'updating hash')
                self.update_commit_hash_in_config(latest_commit_hash)
                self.logger.info("Updating the model...")
                
                progress_root = tk.Tk()
                progress_root.withdraw()  # Hide the main window
                progress_window = tk.Toplevel(progress_root)
                progress_window.title("Updating Model")
                progress_window.geometry("400x100")  # Set the size of the window
                progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')
                progress_bar.pack(pady=20, padx=20) 
                progress_bar.pack(pady=20)
                progress_bar.start()

                update_thread = threading.Thread(target=self.update_model, args=())
                update_thread.start()
                
                while update_thread.is_alive():
                    progress_window.update()
                    progress_window.update_idletasks()
                
                progress_window.destroy()  # Close the progress window after the update completes
                progress_root.destroy()  # Ensure root window is also closed to clean up all GUI components
            else:
                self.logger.info("Update cancelled by the user.")
        else:
            self.logger.info("Your model is up to date.")

        loaded_model_dir = os.path.join(self.model_repo_path, 'model.h5')
        return tf.keras.models.load_model(loaded_model_dir)
    