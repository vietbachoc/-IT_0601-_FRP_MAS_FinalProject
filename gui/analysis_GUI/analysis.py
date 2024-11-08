from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Analysis(parent):
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
        text="Analysis",
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

    global upload_button_image
    upload_button_image = PhotoImage(
        file=relative_to_assets("upload.png")
    )
    Button(
        image=upload_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("upload clicked"),
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    ).place(
        x=495,
        y=590,
        width=228.0,
        height=50.0
    )

    global analysis_button_image
    analysis_button_image = PhotoImage(
        file=relative_to_assets("analysis.png")
    )
    Button(
        image=analysis_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("analysis clicked"),
                relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    ).place(
        x=781,
        y=590,
        width=228.0,
        height=50.0
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