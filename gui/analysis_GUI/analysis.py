from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
import os

# Import backend processing functions
from backend.utils import read_video, save_video
from backend.trackers import Tracker
from backend.team_assigner import TeamAssigner
from backend.player_ball_assigner import PlayerBallAssigner
from backend.camera_movement_estimator import CameraMovementEstimator
from backend.view_transformer import ViewTransformer
from backend.speed_and_distance_estimator import SpeedAndDistance_Estimator
import numpy as np
import cv2

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Global variable
video_path = None

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
    global video_path
    if not video_path:
        messagebox.showerror("No Video Selected", "Please upload a video before running the analysis.")
        return

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
        player_assigner =PlayerBallAssigner()
        team_ball_control= []
        for frame_num, player_track in enumerate(tracks['players']):
            ball_bbox = tracks['ball'][frame_num][1]['bbox']
            assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

            if assigned_player != -1:
                tracks['players'][frame_num][assigned_player]['has_ball'] = True
                team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
            else:
                team_ball_control.append(team_ball_control[-1])
        team_ball_control= np.array(team_ball_control)

        # Draw annotations
        output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
        output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
        speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)

        # Save output video
        output_path = './backend/output_videos/output_video.avi'
        save_video(output_video_frames, output_path)

        messagebox.showinfo("Analysis Complete", f"Analysis complete. Video saved to: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")


def Analysis(parent):
    """
    Create the Analysis UI, including upload and analysis buttons.
    """
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
        command=upload_video,
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
        command=run_analysis,
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