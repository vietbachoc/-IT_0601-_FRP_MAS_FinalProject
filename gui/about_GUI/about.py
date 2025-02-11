from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def About(parent):
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
    
    canvas.create_text(
        28.0,
        40.0,
        anchor="nw",
        text="About",
        fill="#2E236C",
        font=("Lato ExtraBold", 35 * -1)
    )

    canvas.create_rectangle(
        32.0,
        100.0,
        949.0,
        102.0,
        fill="#C8ACD6",
        outline=""
    )

    global about_image_1
    about_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(153.0, 475.0, image=about_image_1)

    global about_image_2
    about_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(815.0, 265.0, image=about_image_2)

    canvas.create_text(
        40.0,
        126.0,
        anchor="nw",
        text="Our Mission",
        fill="#2E236C",
        font=("Lato ExtraBold", 35 * -1)
    )

    canvas.create_text(
        68.0,
        175.0,
        anchor="nw",
        text="Our mission is to revolutionize the way football\nmatch analysis is conducted, providing deeper\ninsights and enhancing decision-making for\ncoaches, analysts, and fans.",
        fill="#2E236C",
        font=("Lato ExtraBold", 25 * -1)
    )

    canvas.create_text(
        283.0,
        384.0,
        anchor="nw",
        text="What we Do",
        fill="#2E236C",
        font=("Lato ExtraBold", 35 * -1)
    )

    canvas.create_text(
        320.0,
        438.0,
        anchor="nw",
        text="The Football Video Analyzer app uses cutting-edge\nAI technology to thoroughly analyze football match\nvideos, delivering detailed statistics, player\nperformance metrics, and strategic insights.",
        fill="#2E236C",
        font=("Lato ExtraBold", 25 * -1)
    )