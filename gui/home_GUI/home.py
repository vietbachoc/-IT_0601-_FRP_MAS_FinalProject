from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class HomeBackground:
    def __init__(self, parent, canvas):
        self.parent = parent
        self.canvas = canvas
        self.CANVAS_WIDTH = 984
        self.CANVAS_HEIGHT = 623
        
        # Define colors for title text based on background
        self.TITLE_COLORS = {
            0: "#2E236C",  # Color for background 1
            1: "#E8DBCB",  # Color for background 2
            2: "#2E236C"   # Color for background 3
        }
        
        self.current_bg = 0
        self.animation_id = None  # Store animation ID
        self.is_running = True    # Control animation state
        
        self.load_images()
        self.setup_canvas()
        self.start_animation()

    def load_images(self):
        background_paths = [
            relative_to_assets("background_1.png"),
            relative_to_assets("background_2.png"), 
            relative_to_assets("background_3.png")
        ]

        self.home_images = []     # Store original images
        self.displayed_images = [] # Store currently displayed images
        
        for path in background_paths:
            pil_image = Image.open(path)
            pil_image = pil_image.resize((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.home_images.append(pil_image)
            self.displayed_images.append(tk_image)

    def setup_canvas(self):
        self.bg_image = self.canvas.create_image(
            self.CANVAS_WIDTH/2,
            self.CANVAS_HEIGHT/2,
            image=self.displayed_images[0],
            anchor="center"
        )

        self.title_text = self.canvas.create_text(
            28.0,
            40.0,
            anchor="nw",
            text="Home",
            fill=self.TITLE_COLORS[0],
            font=("Lato ExtraBold", 35 * -1)
        )

    def create_fade_image(self, image1, image2, alpha):
        fade_image = Image.blend(image1, image2, alpha)
        return ImageTk.PhotoImage(fade_image)

    def change_background(self):
        if not self.is_running:
            return
            
        next_bg = (self.current_bg + 1) % len(self.home_images)
        self.canvas.itemconfig(self.title_text, fill=self.TITLE_COLORS[next_bg])
        
        def perform_fade(step=0, steps=20):
            if not self.is_running or step > steps:
                self.current_bg = next_bg
                self.schedule_next_change()
                return
                
            alpha = step / steps
            fade_img = self.create_fade_image(
                self.home_images[self.current_bg],
                self.home_images[next_bg],
                alpha
            )
            self.temp_image = fade_img  # Prevent garbage collection
            self.canvas.itemconfig(self.bg_image, image=fade_img)
            
            self.animation_id = self.canvas.after(50, lambda: perform_fade(step + 1, steps))
            
        perform_fade()

    def schedule_next_change(self):
        if self.is_running:
            self.animation_id = self.canvas.after(5000, self.change_background)

    def start_animation(self):
        self.is_running = True
        self.schedule_next_change()

    def stop_animation(self):
        self.is_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None

def Home(parent):
    canvas = Canvas(
        parent,
        bg = "#FFFFFF",
        height = 623,
        width = 984,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 260, y = 61)
    
    # Create background handler instance
    bg_handler = HomeBackground(parent, canvas)
    
    # Store background handler in parent for access from other parts of the app
    parent.home_bg_handler = bg_handler
    
    # Bind cleanup to window close
    parent.bind("<Destroy>", lambda e: bg_handler.stop_animation())
    
    return canvas