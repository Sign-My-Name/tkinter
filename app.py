import tkinter as tk
import cv2
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
        self.init_image = cv2.imread("assets/initImage.jpg")
        self.predictor = None
        self.cap = None
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
        self.root.minsize(1200, 720)
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
            "logo_img": ImageTk.PhotoImage(Image.open("new_assets/logo.png").resize((211, 85), Image.LANCZOS)),
            
            # universal images
            "back_img": ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((150, 50), Image.LANCZOS)),
            "spacer" : ImageTk.PhotoImage(Image.open("new_assets/spacer.png").resize((70, 70), Image.LANCZOS)),
            
            # home page images
            "home_page_boy_img": ImageTk.PhotoImage(Image.open("new_assets/homepage_boy.png").resize((400, 500), Image.LANCZOS)),
            "word_identify_img": ImageTk.PhotoImage(Image.open("new_assets/WrdIdentify.png").resize((250, 111), Image.LANCZOS)),
            "name_break_down_img": ImageTk.PhotoImage(Image.open("new_assets/NameBreakDown.png").resize((250, 111), Image.LANCZOS)),
            "identify_img": ImageTk.PhotoImage(Image.open("new_assets/IdentifyPage.png").resize((250, 111), Image.LANCZOS)),
            "sign_a_word_img": ImageTk.PhotoImage(Image.open("new_assets/SignAWord.png").resize((250, 111), Image.LANCZOS)),

            # name breakdown images
            "submit_img": ImageTk.PhotoImage(Image.open("new_assets/submit.png").resize((67, 67), Image.LANCZOS)),
            "next_img": ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS)),
            "what_your_name_img": ImageTk.PhotoImage(Image.open("new_assets/WhatsYourName.png").resize((300, 75), Image.LANCZOS)),
            "congrats" : ImageTk.PhotoImage(Image.open("new_assets/congrats.png").resize((333, 100), Image.LANCZOS)),
            
            # identify page images
            "identify_boy": ImageTk.PhotoImage(Image.open("new_assets/identify_boy.png").resize((400, 500), Image.LANCZOS)),
            "meet_the_letter": ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((250, 62), Image.LANCZOS))
        }

    def create_home_page(self):
        """
        Create the home page UI using configuration loaded from images.
        """
        self.logger.info('starting home page init...')
        home_page_config = {"BG_COLOR": 'peach puff', **self.images}
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
        self.predictor.predict_image(self.init_image)




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
