from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import cv2
import time
import threading
from PIL import Image, ImageTk
import gc

# Import backend processing functions
from backend.utils import read_video, save_video
from backend.trackers import Tracker
from backend.team_assigner import TeamAssigner
from backend.player_ball_assigner import PlayerBallAssigner
from backend.camera_movement_estimator import CameraMovementEstimator
from backend.view_transformer import ViewTransformer
from backend.speed_and_distance_estimator import SpeedAndDistance_Estimator
import numpy as np

# Import global state variables
from gui.scripts.state import set_analyzing_state, get_analyzing_state

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Global variables
video_path = None
output_video_path = "./backend/output_videos/output_video.avi"
video_frame_label = None
video_stream_active = False
cap = None
frame_delay = None
current_frame = None
analyzing_label = None
upload_button = None
analysis_button = None

def upload_video():
    """
    Open a file dialog to allow the user to select a video file.
    """
    global video_path
    video_path = filedialog.askopenfilename(
        title="Select Video",
        filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*")]
    )
    if video_path:
        messagebox.showinfo("File Selected", f"Video selected: {os.path.basename(video_path)}")
    else:
        messagebox.showwarning("No File", "Please select a video file to proceed.")

def run_analysis():
    """
    Perform analysis on the uploaded video using the processing functions.
    """
    global video_path, output_video_path, analyzing_label, video_frame_label
    if not video_path:
        messagebox.showerror("No Video Selected", "Please upload a video before running the analysis.")
        return

    set_analyzing_state(True)

    # Cleanup current video state
    cleanup_current_video()

    # Hide buttons before starting analysis
    hide_buttons()

    # Create analyzing UI components
    analyzing_container = Frame(video_frame_label, bg="#FFFFFF")
    analyzing_container.place(relx=0.5, rely=0.5, anchor="center")
    
    analyzing_label = Label(
        analyzing_container,
        text="Analyzing",
        font=("Lato ExtraBold", 40),
        fg="#2E236C",
        bg="#FFFFFF"
    )
    analyzing_label.pack(pady=(0, 10))

    # Create dots animation
    dots_container = Frame(analyzing_container, bg="#FFFFFF")
    dots_container.pack()
    
    # Load and setup dot images
    image_dot_a = PhotoImage(file=relative_to_assets("dot_a.png"))
    image_dot_b = PhotoImage(file=relative_to_assets("dot_b.png"))
    analyzing_container.dot_a = image_dot_a
    analyzing_container.dot_b = image_dot_b

    dot_labels = []
    for i in range(4):
        dot = Label(
            dots_container,
            image=image_dot_b,
            borderwidth=0,
            highlightthickness=0,
            bg="#FFFFFF"
        )
        dot.pack(side=LEFT, padx=5)
        dot_labels.append(dot)

    def animate_dots():
        if not hasattr(analyzing_container, 'destroyed'):
            current_dot = int(time.time() * 2) % 4
            for i, dot in enumerate(dot_labels):
                dot.configure(image=image_dot_a if i == current_dot else image_dot_b)
            video_frame_label.after(250, animate_dots)

    def analysis_thread():
        try:
            # Read video frames
            video_frames = read_video(video_path)

            # Extract base name of the selected video file (without extension)
            video_base_name = Path(video_path).stem

            # Define the stub paths based on the video file name
            track_stub_path = f'backend/stubs/{video_base_name}_track_stubs.pkl'
            camera_movement_stub_path = f'backend/stubs/{video_base_name}_camera_movement_stub.pkl'

            # Initialize Tracker
            tracker = Tracker('backend/models/football-player-detection.pt')

            tracks = tracker.get_object_tracks(video_frames,
                                            read_from_stub=True,
                                            stub_path=track_stub_path)
            # Get object positions
            tracker.add_position_to_tracks(tracks)

            # Camera movement estimator
            camera_movement_estimator = CameraMovementEstimator(video_frames[0])
            camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                                    read_from_stub=True,
                                                                                    stub_path=camera_movement_stub_path)
            camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

            # View Trasnformer
            view_transformer = ViewTransformer()
            view_transformer.add_transformed_position_to_tracks(tracks)

            # Interpolate Ball Positions
            tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

            # Speed and distance estimator
            speed_and_distance_estimator = SpeedAndDistance_Estimator()
            speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)

            # Assign Player Teams
            team_assigner = TeamAssigner()
            team_assigner.assign_team_color(video_frames[0], 
                                            tracks['players'][0])
            
            for frame_num, player_track in enumerate(tracks['players']):
                for player_id, track in player_track.items():
                    team = team_assigner.get_player_team(video_frames[frame_num],   
                                                        track['bbox'],
                                                        player_id)
                    tracks['players'][frame_num][player_id]['team'] = team 
                    tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

            # Assign Ball Aquisition
            player_assigner = PlayerBallAssigner()
            team_ball_control = []
            
            # Find the first frame where the player has the ball and initialize the initial state
            initial_frame = 0
            current_possession = None
            
            # Find the initial ball control state in the first 10 frames
            for frame_num in range(min(10, len(tracks['players']))):
                ball_bbox = tracks['ball'][frame_num][1]['bbox']
                assigned_player = player_assigner.assign_ball_to_player(tracks['players'][frame_num], ball_bbox)
                
                if assigned_player != -1:
                    current_possession = tracks['players'][frame_num][assigned_player]['team']
                    initial_frame = frame_num
                    break
            
            # Fill frames from start to found frame
            team_ball_control.extend([current_possession] * (initial_frame + 1))
            
            # Process remaining frames with small buffers to avoid sudden changes
            possession_buffer = []
            BUFFER_SIZE = 3
            
            for frame_num in range(initial_frame + 1, len(tracks['players'])):
                ball_bbox = tracks['ball'][frame_num][1]['bbox']
                assigned_player = player_assigner.assign_ball_to_player(tracks['players'][frame_num], ball_bbox)

                if assigned_player != -1:
                    tracks['players'][frame_num][assigned_player]['has_ball'] = True
                    new_possession = tracks['players'][frame_num][assigned_player]['team']
                    possession_buffer.append(new_possession)
                else:
                    possession_buffer.append(current_possession)
                    
                # Only update possession when buffer is large enough and consistent
                if len(possession_buffer) >= BUFFER_SIZE:
                    most_common = max(set(possession_buffer), key=possession_buffer.count)
                    if possession_buffer.count(most_common) >= BUFFER_SIZE - 1:
                        current_possession = most_common
                    possession_buffer.pop(0)
                    
                team_ball_control.append(current_possession)
            
            # Convert to numpy array for more efficient processing
            team_ball_control = np.array(team_ball_control)

            # Draw annotations
            output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
            output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
            speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)

            # Save output video
            save_video(output_video_frames, output_video_path)

            # After analysis is complete
            video_frame_label.after(0, lambda: complete_analysis(analyzing_container))
        except Exception as e:
            video_frame_label.after(0, lambda: show_error(analyzing_container, str(e)))

    def complete_analysis(container):
        set_analyzing_state(False)
        container.destroyed = True
        container.destroy()
        messagebox.showinfo("Analysis Complete", f"Analysis complete. Video saved to: {output_video_path}")
        show_buttons()
        display_video()
        cleanup_memory()

    def show_error(container, error_message):
        set_analyzing_state(False)
        container.destroyed = True
        container.destroy()
        messagebox.showerror("Error", f"An error occurred during analysis: {error_message}")

    # Start animation and analysis thread
    video_frame_label.update()
    animate_dots()
    analysis_thread = threading.Thread(target=analysis_thread)
    analysis_thread.daemon = True
    analysis_thread.start()
    cleanup_memory()

def display_video():
    """
    Display the processed video in the fixed area on the Analysis page.
    """
    global video_stream_active, cap, frame_delay, current_frame, video_frame_label
    
    # Ensure video frame label is visible
    video_frame_label.configure(bg="white")
    
    if cap is None:
        cap = cv2.VideoCapture(output_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = int(1000/fps)
        video_stream_active = True
        update_frame()
    elif not video_stream_active and current_frame is not None:
        # Display saved frame when returning to paused video
        display_frame(current_frame)

def display_frame(frame):
    """
    Display a single frame with proper sizing
    """
    if video_frame_label.winfo_width() == 1282:
        frame = cv2.resize(frame, (1282, 722))
    else:
        frame = cv2.resize(frame, (915, 373))
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img_tk = ImageTk.PhotoImage(image=img)
    video_frame_label.imgtk = img_tk
    video_frame_label.configure(image=img_tk)

def update_frame():
    global video_stream_active, cap, frame_delay, current_frame
    if not video_stream_active or cap is None:
        return
        
    ret, frame = cap.read()
    if ret:
        current_frame = frame.copy()
        display_frame(current_frame)
        video_frame_label.after_id = video_frame_label.after(frame_delay, update_frame)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        video_frame_label.after_id = video_frame_label.after(frame_delay, update_frame)

def pause_video():
    """
    Toggle video pause/resume
    """
    global video_stream_active
    video_stream_active = not video_stream_active
    if video_stream_active:
        update_frame()

def restart_video():
    global cap
    if cap is not None:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

def toggle_fullscreen():
    global video_frame_label, cap
    if video_frame_label.winfo_width() == 915:  # Normal size
        video_frame_label.place(x=0, y=0, width=1282, height=722)
        video_frame_label.configure(bg="white")
        video_frame_label.lift()
        
        # Resize current frame if video is paused
        if cap is not None and not video_stream_active:
            current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos - 1)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (1282, 722))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)
                video_frame_label.imgtk = img_tk
                video_frame_label.configure(image=img_tk)
    else:  # Normal size
        video_frame_label.place(x=294, y=186, width=915, height=373)
        video_frame_label.configure(bg="white")
        
        # Resize current frame if video is paused
        if cap is not None and not video_stream_active:
            current_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos - 1)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (915, 373))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)
                video_frame_label.imgtk = img_tk
                video_frame_label.configure(image=img_tk)

def stop_video_stream():
    """
    Stop the video stream when navigating away from the Analysis page.
    """
    global video_stream_active, video_frame_label, current_frame, cap
    video_stream_active = False
    
    if hasattr(video_frame_label, 'after_id'):
        video_frame_label.after_cancel(video_frame_label.after_id)
    
    # Capture current frame before stopping
    if cap is not None and video_frame_label is not None:
        ret, frame = cap.read()
        if ret:
            current_frame = frame.copy()
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

def cleanup_current_video():
    """
    Cleanup current video state before starting new analysis
    """
    global video_stream_active, cap, current_frame
    
    # Stop video if playing
    video_stream_active = False
    
    # Cancel any pending frame updates
    if hasattr(video_frame_label, 'after_id'):
        video_frame_label.after_cancel(video_frame_label.after_id)
    
    # Release current video capture
    if cap is not None:
        cap.release()
        cap = None
    
    # Clear current frame
    current_frame = None
    
    # Clear video display
    if video_frame_label is not None:
        video_frame_label.configure(image='')

def cleanup_memory():
    global video_frames, tracks, camera_movement_per_frame, output_video_frames
    video_frames = None
    tracks = None
    camera_movement_per_frame = None
    output_video_frames = None

    # Call garbage collector
    gc.collect()

def Analysis(parent):
    """
    Create the Analysis UI, including upload and analysis buttons.
    """
    global video_frame_label, current_frame, upload_button, analysis_button
    
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
    upload_button = Button(
        image=upload_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=upload_video,
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    )
    upload_button.place(
        x=495,
        y=590,
        width=228.0,
        height=50.0
    )

    global analysis_button_image
    analysis_button_image = PhotoImage(
        file=relative_to_assets("analysis.png")
    )
    analysis_button = Button(
        image=analysis_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=run_analysis,
        relief="flat",
        bg='#FFFFFF',
        activebackground='#FFFFFF'
    )
    analysis_button.place(
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

    # Add key bindings
    parent.bind('p', lambda e: pause_video())
    parent.bind('r', lambda e: restart_video())
    parent.bind('f', lambda e: toggle_fullscreen())
    
    # Video display area
    video_frame_label = Label(parent, bg="#FFFFFF")
    video_frame_label.place(x=294, y=186, width=915, height=373)
    
    # If we have a saved frame, display it
    if current_frame is not None:
        display_frame(current_frame)
    
    return canvas

def hide_buttons():
    """Hide upload and analysis buttons"""
    global upload_button, analysis_button
    if upload_button:
        upload_button.place_forget()
    if analysis_button:
        analysis_button.place_forget()

def show_buttons():
    """Show upload and analysis buttons"""
    global upload_button, analysis_button
    if upload_button:
        upload_button.place(
            x=495,
            y=590,
            width=228.0,
            height=50.0
        )
    if analysis_button:
        analysis_button.place(
            x=781,
            y=590,
            width=228.0,
            height=50.0
        )