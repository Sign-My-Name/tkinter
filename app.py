import tkinter as tk
import cv2
import pygame
from PIL import ImageTk, Image
from predictor import predictor
from proj_camera import proj_camera
from proj_logger import get_logger
from UI.home_page import HomePage

class App:
    def __init__(self, root):
        """
        Initialize the application with the main window root, setup logging, UI, camera, and predictor.
        Args:
            root: The main tkinter window.
        """
        self.logger = get_logger()
        self.logger.info('starting app init...')
        self.root = root
        pygame.mixer.init()
        self.bg_music = pygame.mixer.Sound(f'./sounds/BG_music.ogg')
        self.bg_music.set_volume(0.18)
        self.init_image = cv2.imread("assets/initImage.jpg")
        self.predictor = None
        self.cap = None
        self.welcome_sound = pygame.mixer.Sound(f'./sounds/welcome.ogg')
        self.welcome_sound.play(0)
        self.start_camera()
        self.start_predictor()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the main user interface for the application.
        """
        self.logger.info('starting UI init...')
        self.root.title("SignMyName")
        self.root.configure(bg='black')
        self.root.minsize(1200, 750)
        self.root.iconbitmap("assets/icon.ico")
        self.load_images()
        self.create_home_page()

    def load_images(self):
        """
        Load and resize images for the UI.
        """
        self.logger.info('starting image init...')
        self.images = {
            # logo
            "logo_img": ImageTk.PhotoImage(Image.open("assets/logo.png").resize((211, 85), Image.LANCZOS)),
            
            # universal images
            "back_img": ImageTk.PhotoImage(Image.open("assets/back.png").resize((180, 60), Image.LANCZOS)),
            "spacer" : ImageTk.PhotoImage(Image.open("assets/spacer.png").resize((70, 70), Image.LANCZOS)),
            "clock" : ImageTk.PhotoImage(Image.open("assets/Clock.png").resize((300,300), Image.LANCZOS)),
            
            # home page images
            "home_page_boy_img": ImageTk.PhotoImage(Image.open("assets/homepage_boy.png").resize((400, 500), Image.LANCZOS)),
            "word_identify_img": ImageTk.PhotoImage(Image.open("assets/WrdIdentify.png").resize((250, 111), Image.LANCZOS)),
            "learn_a_letter_img": ImageTk.PhotoImage(Image.open("assets/LearnALetter.png").resize((250, 111), Image.LANCZOS)),
            "identify_img": ImageTk.PhotoImage(Image.open("assets/IdentifyPage.png").resize((250, 111), Image.LANCZOS)),
            "sign_a_word_img": ImageTk.PhotoImage(Image.open("assets/SignAWord.png").resize((250, 111), Image.LANCZOS)),

            # learn a letter images
            "submit_img": ImageTk.PhotoImage(Image.open("assets/submit.png").resize((67, 67), Image.LANCZOS)),
            "learn_a_letter_boy" : ImageTk.PhotoImage(Image.open("assets/learn_a_letter_boy.png").resize((360, 250), Image.LANCZOS)),
            "learn_a_letter_try_again" : ImageTk.PhotoImage(Image.open("assets/learn_a_letter_try_again.png").resize((360, 250), Image.LANCZOS)),
            "learn_a_letter_only_hebrew" : ImageTk.PhotoImage(Image.open("assets/learn_a_letter_only_hebrew.png").resize((360, 250), Image.LANCZOS)),
            "what_your_name_img": ImageTk.PhotoImage(Image.open("assets/WhatsYourName.png").resize((300, 75), Image.LANCZOS)),

            # identify page images
            "identify_boy": ImageTk.PhotoImage(Image.open("assets/identify_boy.png").resize((360, 250), Image.LANCZOS)),
            "meet_the_letter": ImageTk.PhotoImage(Image.open("assets/meet_the_letter.png").resize((312, 75), Image.LANCZOS)),

            # sign a word images
            "last_letter": ImageTk.PhotoImage(Image.open("assets/sign_a_word_last_letter.png").resize((405, 98), Image.LANCZOS)),
            "finished_word": ImageTk.PhotoImage(Image.open("assets/sign_a_word_finished_word.png").resize((405, 98), Image.LANCZOS)),
            "sign_a_word_boy": ImageTk.PhotoImage(Image.open("assets/sign_a_word_boy.png").resize((400, 500), Image.LANCZOS)),
            "backspace_img": ImageTk.PhotoImage(Image.open("assets/sign_a_word_back_space.png").resize((180, 60), Image.LANCZOS)),


            # word identify page images
            "word_identify_boy" : ImageTk.PhotoImage(Image.open("assets/word_identify_boy.png").resize((400, 500), Image.LANCZOS)),
            "meet_the_word": ImageTk.PhotoImage(Image.open("assets/meet_the_word.png").resize((312, 75), Image.LANCZOS))
        }

    def create_home_page(self):
        """
        Create the home page UI using configuration loaded from images.
        """
        self.logger.info('starting home page init...')
        home_page_config = {"BG_COLOR": 'peach puff', **self.images, "stop_BG_music": self.stop_BG_music, "start_BG_music": self.start_BG_music}
        self.home_page = HomePage(self.root, home_page_config)

    def start_camera(self):
        """
        Initialize camera capture and process the initial image.
        """
        self.logger.info('starting camera init...')
        self.cap = proj_camera()
        self.init_image = self.cap.cut_image(self.init_image, (128,128))

    def start_predictor(self):
        """
        Initialize the image predictor and start prediction on the initial image.
        """
        self.logger.info('starting predictor init...')
        self.predictor = predictor()
        self.predictor.predict_image(self.init_image, "letters")

    def start_BG_music(self):
        self.bg_music.play(-1)
    
    def stop_BG_music(self):
        self.bg_music.stop()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.start_BG_music()
    root.mainloop()
    app.stop_BG_music()
