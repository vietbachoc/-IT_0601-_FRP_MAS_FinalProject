from pathlib import Path
from tkinter import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Statistics(parent):
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
        text="Statistics",
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

    canvas.create_text(
        384.0,
        152.0,
        anchor="nw",
        text="Match Statistics",
        fill="#2E236C",
        font=("Lato ExtraBold", 30 * -1)
    )

    global statistics_image_1
    statistics_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(174.0, 241.0, image=statistics_image_1)

    global statistics_image_2
    statistics_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(808.0, 241.0, image=statistics_image_2)

    canvas.create_text(
        100.0,
        230.0,
        anchor="nw",
        text="Ball Possession ",
        fill="#FFFFFF",
        font=("Lato Bold", 22 * -1)
    )

    canvas.create_text(
        734.0,
        230.0,
        anchor="nw",
        text="Ball Possession ",
        fill="#FFFFFF",
        font=("Lato Bold", 22 * -1)
    )

    canvas.create_text(
        338.0,
        280.0,
        anchor="nw",
        text="3",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        438.0,
        280.0,
        anchor="nw",
        text="Shots On Target",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        623.0,
        280.0,
        anchor="nw",
        text="2",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        338.0,
        341.0,
        anchor="nw",
        text="3",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        338.0,
        402.0,
        anchor="nw",
        text="3",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        338.0,
        463.0,
        anchor="nw",
        text="3",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        623.0,
        341.0,
        anchor="nw",
        text="2",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        623.0,
        402.0,
        anchor="nw",
        text="2",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        623.0,
        463.0,
        anchor="nw",
        text="2",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_rectangle(
        349.0,
        305.0,
        634.0,
        313.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        349.0,
        366.0,
        634.0,
        374.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        349.0,
        427.0,
        634.0,
        435.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        349.0,
        488.0,
        634.0,
        496.0,
        fill="#D9D9D9",
        outline="")
    
    global statistics_image_3
    statistics_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    canvas.create_image(174.0, 417.0, image=statistics_image_3)

    global statistics_image_4
    statistics_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    canvas.create_image(809.0, 417.0, image=statistics_image_4)

    global statistics_percent_1
    statistics_percent_1 = PhotoImage(file=relative_to_assets("percent_1.png"))
    canvas.create_image(129.0, 389.0, image=statistics_percent_1)

    canvas.create_text(
        139.0,
        389.0,
        anchor="nw",
        text="40",
        fill="#C8ACD6",
        font=("Lato Bold", 60 * -1)
    )

    global statistics_percent_2
    statistics_percent_2 = PhotoImage(file=relative_to_assets("percent_2.png"))
    canvas.create_image(764.0, 389.0, image=statistics_percent_2)

    canvas.create_text(
        774.0,
        389.0,
        anchor="nw",
        text="60",
        fill="#443D8B",
        font=("Lato Bold", 60 * -1)
    )

    canvas.create_text(
        438.0,
        341.0,
        anchor="nw",
        text="Shots Off Target",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        449.0,
        402.0,
        anchor="nw",
        text="Corner Kicks",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_text(
        466.0,
        463.0,
        anchor="nw",
        text="Passing",
        fill="#2E236C",
        font=("Lato Bold", 15 * -1)
    )

    canvas.create_rectangle(
        32.0,
        100.0,
        949.0,
        102.0,
        fill="#C8ACD6",
        outline=""
    )