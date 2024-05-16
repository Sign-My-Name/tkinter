from proj_logger import get_logger
from predictor import predictor

import cv2
import threading
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk


class proj_camera:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(proj_camera, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.logger = get_logger()
            self.logger.info(f'init camera...')
            self.cap = None
            self.keep_running = False
            self.img_ref = None

            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles

            self.model = predictor()
    
    def start_camera(self, video_label, prediction_label, q = None):
        self.logger.info(f'starting camera')
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.keep_running = True
            self.frame_counter = 0
            self.video_label = video_label
            self.logger.info("Camera is initialized!")
            self.camera_thread = threading.Thread(target=self.update_video,
                                                  args=(prediction_label, q),
                                                  daemon=True)
            self.camera_thread.start()

    def close_camera(self):
        self.logger.info(f'closing camera')
        self.keep_running = False
        if self.camera_thread and self.camera_thread.is_alive:
            self.cap.release()
            self.camera_thread.join(timeout=1)  # Wait for the camera thread to finish
            self.logger.info(f'Releasing camera!') # If thread is still alive, force terminate

    def cut_image(self, image, size=None):
        image = image.astype(np.uint8)
        processed_image = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
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
            hand_region_bgr = cv2.resize(hand_region_uint8, dsize=size)
        else:
            hand_region_bgr = None
        return hand_region_bgr
    
    def draw_hand_skeleton(self, image):
        results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            annotated_image = image.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
            return annotated_image
        return image

    def isolate_and_crop_hand(self, image, padding=60):
        results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            image = self.draw_hand_skeleton(image)
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
    
    def update_video(self, prediction_label, q = None):
        # global No_hands_flag
        counter_for_None_hands = 0
        # No_hands_flag = 0
        while self.keep_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.img_ref = img  # Maintain a reference
                self.video_label.configure(image=self.img_ref)
                self.video_label.image = self.img_ref

                self.frame_counter += 1
                if self.frame_counter % 5 == 0:
                    processed_frame = self.cut_image(frame, (128,128))
                    ## TODO: find a solution for no hands count + no hands flag
                    # if processed_frame is None:
                    #     counter_for_None_hands += 1
                    # else:
                    #     counter_for_None_hands = 0
                    # if counter_for_None_hands >= 30:
                    #     No_hands_flag = 1
                    # else:
                    #     No_hands_flag = 0
                    
                    prediction = self.model.predict_image(processed_frame)
                    if float(prediction[1]) > 0.60:
                        prediction_label.config(text=prediction[0])
                        if q is not None:
                            q.push(prediction[0])
            else:
                continue
