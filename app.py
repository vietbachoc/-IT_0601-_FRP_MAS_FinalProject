from tkinter import *
from pathlib import Path
from gui.home_GUI.home import Home
from gui.analysis_GUI.analysis import Analysis, output_video_path, stop_video_stream
from gui.statistics_GUI.statistics import Statistics
from gui.about_GUI.about import About
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./gui/assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ~ FUNCTIONS FOR BUTTONS FOR CHANGING TABS ~ #
def handle_button_press(btn_name):
    global current_window
    reset_button_images()

    # Stop video if leaving analysis page
    if hasattr(current_window, 'stop_video_stream'):
        current_window.stop_video_stream()

    if btn_name == "home":
        home_button.config(image=home_button_active_image)
        current_window = Home(window)
    elif btn_name == "analysis":
        analysis_button.config(image=analysis_button_active_image)
        current_window = Analysis(window)
        # Restart video if returning to analysis page
        if hasattr(current_window, 'display_video') and os.path.exists(output_video_path):
            current_window.display_video()
    elif btn_name == "statistics":
        statistics_button.config(image=statistics_button_active_image)
        current_window = Statistics(window)
    elif btn_name == "about":
        about_button.config(image=about_button_active_image)
        current_window = About(window)

def reset_button_images():
    home_button.config(image=home_button_default_image)
    analysis_button.config(image=analysis_button_default_image)
    statistics_button.config(image=statistics_button_default_image)
    about_button.config(image=about_button_default_image)


window = Tk()
window.title("Football Analysis")
window.geometry("1282x722")
window.configure(bg="#17153B")

'''For Icon'''
# window.iconbitmap(relative_to_assets("icon.ico"))

canvas = Canvas(
    window,
    bg="#17153B",
    height=722,
    width=1282,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
background_image = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    752.0,
    372.0,
    image=background_image
)

current_window = Home(window)

############### APP NAME ###############
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    124.0,
    100.0,
    image=image_image_2
)
########################################

############### HOME BUTTON ###############
home_button_active_image = PhotoImage(file=relative_to_assets("home_1.png"))
home_button_default_image = PhotoImage(file=relative_to_assets("home.png"))
home_button = Button(
    image=home_button_active_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("home"),
    relief="flat",
    activebackground="#17153B",
    activeforeground="#17153B"
)
home_button.place(
    x=15.0,
    y=254.0,
    width=220.0,
    height=48.0
)
###########################################

############# ANALYSIS BUTTON #############
analysis_button_default_image = PhotoImage(file=relative_to_assets("analysis.png"))
analysis_button_active_image = PhotoImage(file=relative_to_assets("analysis_1.png"))
analysis_button = Button(
    image=analysis_button_default_image,
    bg="#17153B",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("analysis"),
    relief="flat",
    activebackground="#17153B",
    activeforeground="#17153B"
)
analysis_button.place(
    x=15.0,
    y=317.0,
    width=220.0,
    height=48.0
)
###########################################

############# STATISTICS BUTTON #############
statistics_button_default_image = PhotoImage(file=relative_to_assets("statistics.png"))
statistics_button_active_image = PhotoImage(file=relative_to_assets("statistics_1.png"))
statistics_button = Button(
    image=statistics_button_default_image,
    bg="#17153B",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("statistics"),
    relief="flat",
    activebackground="#17153B",
    activeforeground="#17153B"
)
statistics_button.place(
    x=15.0,
    y=380.0,
    width=220.0,
    height=48.0
)
###########################################

############## ABOUT BUTTON ##############
about_button_default_image = PhotoImage(file=relative_to_assets("about.png"))
about_button_active_image = PhotoImage(file=relative_to_assets("about_1.png"))
about_button = Button(
    image=about_button_default_image,
    bg="#17153B",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: handle_button_press("about"),
    relief="flat",
    activebackground="#17153B",
    activeforeground="#17153B"
)
about_button.place(
    x=15.0,
    y=443.0,
    width=220.0,
    height=48.0
)
##########################################

window.resizable(False, False)
window.mainloop()
