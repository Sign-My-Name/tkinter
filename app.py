import tkinter as tk
import cv2
from predictor import predictor
from proj_camera import proj_camera
from proj_logger import get_logger
from PIL import ImageTk, Image
from UI.home_page import HomePage

class App:
    def __init__(self, root):
        self.logger = get_logger()
        self.logger.info(f'starting app init...')
        self.root = root
        self.init_image = cv2.imread("assets/initImage.jpg")
        self.predictor = None
        self.cap = None
        self.start_camera()
        self.start_predictor()
        self.setup_ui()

    def setup_ui(self):
        self.logger.info(f'starting UI init...')
        self.root.title("SignMyName")
        self.root.configure(bg='black')
        self.root.minsize(1200, 720)
        self.root.iconbitmap("assets/icon.ico")
        self.load_images()
        self.create_home_page()

    def load_images(self):
        self.logger.info(f'starting image init...')
        self.images = {
            "logo_img": ImageTk.PhotoImage(Image.open("assets/logo.png").resize((423, 171), Image.LANCZOS)),
            "back_img": ImageTk.PhotoImage(Image.open("new_assets/back.png").resize((250, 62), Image.LANCZOS)),
            "home_page_boy_img": ImageTk.PhotoImage(Image.open("new_assets/homepage_boy.png").resize((450, 450), Image.LANCZOS)),
            "word_identify_img": ImageTk.PhotoImage(Image.open("new_assets/WrdIdentify.png").resize((250, 250), Image.LANCZOS)),
            "name_break_down_img": ImageTk.PhotoImage(Image.open("new_assets/NameBreakDown.png").resize((250, 250), Image.LANCZOS)),
            "identify_img": ImageTk.PhotoImage(Image.open("new_assets/IdentifyPage.png").resize((250, 250), Image.LANCZOS)),
            "sign_a_word_img": ImageTk.PhotoImage(Image.open("new_assets/SignAWord.png").resize((250, 250), Image.LANCZOS)),
            "submit_img": ImageTk.PhotoImage(Image.open("assets/submit.png").resize((124, 67), Image.LANCZOS)),
            "next_img": ImageTk.PhotoImage(Image.open("assets/next.png").resize((154, 68), Image.LANCZOS)),
            "identify_boy_bubble": ImageTk.PhotoImage(Image.open("new_assets/boy_bubble.png").resize((400, 500), Image.LANCZOS)),
            "meet_the_letter": ImageTk.PhotoImage(Image.open("new_assets/meet_the_letter.png").resize((250, 62), Image.LANCZOS))
        }

    def create_home_page(self):
        self.logger.info(f'starting home page init...')
        home_page_config = {
            "BG_COLOR": 'peach puff',
            **self.images
        }
        self.home_page = HomePage(self.root, home_page_config)

    def start_camera(self):
        self.logger.info(f'starting camera init...')
        self.cap = proj_camera()
        self.init_image = self.cap.cut_image(self.init_image, (128,128))

    def start_predictor(self):
        self.logger.info(f'starting predictor init...')
        self.predictor = predictor()
        self.predictor.predict_image(self.init_image)



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
