from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
    
    image_1_path = relative_to_assets("image_1.png")
    image_2_path = relative_to_assets("image_2.png")
    image_3_path = relative_to_assets("image_3.png")

    parent.images = []

    image_image_1 = PhotoImage(file=image_1_path)
    parent.images.append(image_image_1)
    canvas.create_image(240.0, 305.0, image=image_image_1)

    image_image_2 = PhotoImage(file=image_2_path)
    parent.images.append(image_image_2)
    canvas.create_image(767.0, 322.0, image=image_image_2)

    image_image_3 = PhotoImage(file=image_3_path)
    parent.images.append(image_image_3)
    canvas.create_image(500.0, 305.0, image=image_image_3)

    canvas.create_text(
        28.0,
        40.0,
        anchor="nw",
        text="Home",
        fill="#2E236C",
        font=("Montserrat SemiBold", 35 * -1)
    )

    ############# Greetings/Hello #############
    from gui.scripts.greetings import greet
    canvas.create_text(
        800.0,
        40.0,
        anchor="nw",
        text=greet(),
        fill="#2E236C",
        font=("Montserrat SemiBold", 35 * -1)
    )
    ###########################################
