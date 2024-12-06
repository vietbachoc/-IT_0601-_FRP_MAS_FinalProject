from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

from gui.scripts.statistics_state import get_team_statistics
from gui.analysis_GUI.analysis import video_path


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class StatisticsGUI:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = self._create_canvas()
        self.images = []
        self._initialize_ui()

    def _create_canvas(self) -> Canvas:
        canvas = Canvas(
            self.parent,
            bg="#FFFFFF",
            height=623,
            width=984,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=260, y=61)
        return canvas

    def _initialize_ui(self):
        self._create_static_elements()
        self._create_dynamic_elements()
        self._create_save_button()

    def _create_static_elements(self):
        # Title
        self.canvas.create_text(
            28.0,
            40.0,
            anchor="nw",
            text="Statistics",
            fill="#2E236C",
            font=("Lato ExtraBold", 35 * -1)
        )
        # Divider
        self.canvas.create_rectangle(
            32.0,
            100.0,
            949.0,
            102.0,
            fill="#C8ACD6",
            outline=""
        )
        # # Team Labels
        # self.canvas.create_text(
        #     209.0,
        #     164.0,
        #     anchor="nw",
        #     text="Team 1",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 22 * -1)
        # )
        # self.canvas.create_text(
        #     574.0,
        #     164.0,
        #     anchor="nw",
        #     text="Team 2",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 22 * -1)
        # )
        # # Possession Labels
        # self.canvas.create_text(
        #     369.0,
        #     184.0,
        #     anchor="nw",
        #     text="Possession",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 10 * -1)
        # )
        # self.canvas.create_text(
        #     736.0,
        #     184.0,
        #     anchor="nw",
        #     text="Possession",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 10 * -1)
        # )

    def _create_dynamic_elements(self):
        # Create Images
        self._create_images()

        # Get Statistics Data
        stats = get_team_statistics()

        # Determine Possession Colors and Icons
        team1_possession = stats[1]['possession']
        team2_possession = stats[2]['possession']

        if team1_possession >= team2_possession:
            team1_color = "#9EFF88"  # Green
            team2_color = "#FF8080"  # Red
            team1_icon = "Up.png"
            team2_icon = "Down.png"
        else:
            team1_color = "#FF8080"  # Red
            team2_color = "#9EFF88"  # Green
            team1_icon = "Down.png"
            team2_icon = "Up.png"

        # Possession Values
        self.canvas.create_text(
            367.0,
            159.0,
            anchor="nw",
            text=f"{team1_possession:.1f}%",
            fill=team1_color,
            font=("Inter Bold", 18 * -1)
        )
        self.canvas.create_text(
            734.0,
            159.0,
            anchor="nw",
            text=f"{team2_possession:.1f}%",
            fill=team2_color,
            font=("Inter Bold", 18 * -1)
        )

        # Create Icons
        self._create_icons(team1_icon, team2_icon)

        # Create Charts and Table
        self.speed_chart_fig = self._create_speed_chart()
        self.speed_chart_canvas = FigureCanvasTkAgg(
            self.speed_chart_fig, self.canvas)
        self.speed_chart_canvas.draw()
        self.speed_chart_canvas.get_tk_widget().place(
            x=69, y=259, width=252, height=288)
        self.canvas.chart_canvas = self.speed_chart_canvas

        self.radar_chart_fig = self._create_radar_chart()
        self.radar_chart_canvas = FigureCanvasTkAgg(
            self.radar_chart_fig, self.canvas)
        self.radar_chart_canvas.draw()
        self.radar_chart_canvas.get_tk_widget().place(
            x=663, y=259, width=252, height=288)
        self.canvas.radar_chart_canvas = self.radar_chart_canvas

        # Create Player Statistics Table
        self.player_stats_table = self._create_player_stats_table()

    def _create_images(self):
        image_files = [
            ("Team_1.png", 308.0, 175.0),
            ("Team_2.png", 675.0, 175.0),
            ("image_3.png", 195.0, 403.0),
            ("image_4.png", 492.0, 403.0),
            ("image_5.png", 789.0, 403.0),
            ("image_6.png", 195.0, 162.0),
            ("image_7.png", 562.0, 162.0)
        ]
        for file_name, x, y in image_files:
            image = self._create_and_store_image(file_name, x, y)
            self.images.append(image)

    def _create_and_store_image(self, file_name: str, x: float, y: float) -> PhotoImage:
        image = PhotoImage(file=relative_to_assets(file_name))
        self.canvas.create_image(x, y, image=image)
        return image  # Keep reference

    def _create_icons(self, team1_icon: str, team2_icon: str):
        icon_positions = [
            (team1_icon, 349.0, 170.0),
            (team2_icon, 716.0, 171.0)
        ]
        for icon, x, y in icon_positions:
            image = self._create_and_store_image(icon, x, y)
            self.images.append(image)

    def _create_speed_chart(self) -> plt.Figure:
        stats = get_team_statistics()
        fig, ax = plt.subplots(figsize=(2.8, 2.5), facecolor='#433D8B')
        ax.set_facecolor('#433D8B')

        teams = ['Team 1', 'Team 2']
        speeds = [stats[1]['avg_speed'], stats[2]['avg_speed']]
        x = np.arange(len(teams))
        bars = ax.bar(x, speeds, width=0.4)

        # Customize bar colors
        bars[0].set_color('#9EFF88' if speeds[0] >= speeds[1] else '#FF8080')
        bars[1].set_color('#9EFF88' if speeds[1] > speeds[0] else '#FF8080')

        # Customize chart appearance
        ax.set_ylabel('Speed (km/h)', color='white')
        ax.set_title('Average Speed of Players', fontsize=11,
                     color='white', fontweight='bold', pad=14)
        ax.set_xticks(x)
        ax.set_xticklabels(teams, color='white')
        ax.tick_params(axis='both', colors='white')

        for spine in ax.spines.values():
            spine.set_color('white')

        # Add value labels
        max_speed = max(speeds) or 1
        y_max = np.ceil(max_speed) + 1.5 if max_speed > 0 else 1.5
        ax.set_ylim(0, max(y_max, 0.1))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))
        plt.subplots_adjust(top=0.85, left=0.3)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + (y_max * 0.02),
                    f'{height:.1f}', ha='center', va='bottom', color='white')

        return fig

    def _create_radar_chart(self) -> plt.Figure:
        stats = get_team_statistics()
        categories = ['Distance', 'Avg Speed', 'Ball Controls']
        team1_values = [
            stats[1]['total_distance'],
            stats[1]['avg_speed'],
            stats[1]['num_ball_controls']
        ]
        team2_values = [
            stats[2]['total_distance'],
            stats[2]['avg_speed'],
            stats[2]['num_ball_controls']
        ]

        # Normalize data
        max_values = [max(team1_values[i], team2_values[i], 1)
                      for i in range(len(categories))]
        team1_values = [v / max_values[i]
                        for i, v in enumerate(team1_values)]
        team2_values = [v / max_values[i]
                        for i, v in enumerate(team2_values)]

        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
        team1_values += team1_values[:1]
        team2_values += team2_values[:1]
        angles = np.concatenate((angles, [angles[0]]))

        fig = plt.figure(figsize=(3.2, 3.2), facecolor='#433D8B')
        ax = fig.add_subplot(111, polar=True)
        ax.set_facecolor('#433D8B')

        ax.set_xticklabels([])

        label_position = 1.1
        for i, (angle, label) in enumerate(zip(angles[:-1], categories)):
            ha, va, rotation = 'center', 'center', 15
            label_pos = label_position

            if i == 0:  # Distance
                ha, va, rotation = 'right', 'bottom', -72
                label_pos *= 1.1
            elif i == 1:  # Avg Speed
                ha, va, rotation = 'center', 'bottom', 25
                label_pos *= 1.05
            else:  # Ball Controls
                ha, va, rotation = 'center', 'top', -25
                label_pos *= 1.05

            ax.text(angle, label_pos, label, color='white',
                    fontsize=8, fontweight='bold',
                    ha=ha, va=va,
                    rotation=rotation,
                    rotation_mode='anchor')

        ax.set_yticklabels([])
        ax.xaxis.grid(False)
        ax.yaxis.grid(True, color='white', alpha=0.2, linewidth=0.3)
        ax.set_ylim(0, 1.1)
        plt.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.85)

        # Plot data
        ax.plot(angles, team1_values, color='#9EFF88',
                linewidth=2, linestyle='solid', label='Team 1')
        ax.fill(angles, team1_values, color='#9EFF88', alpha=0.25)

        ax.plot(angles, team2_values, color='#FF8080',
                linewidth=2, linestyle='solid', label='Team 2')
        ax.fill(angles, team2_values, color='#FF8080', alpha=0.25)

        # Add Title and Legend
        fig.suptitle('Team Comparison', color='white',
                     size=11, fontweight='bold', y=0.95)
        ax.legend(loc='lower right',
                  bbox_to_anchor=(1.18, -0.25),
                  fontsize=8, facecolor='#433D8B',
                  edgecolor='white', framealpha=0.8,
                  labelcolor='white')

        return fig

    def _create_player_stats_table(self) -> ttk.Treeview:
        columns = ("Player ID", "Avg Speed", "Ball Controls")
        table = ttk.Treeview(
            self.canvas, columns=columns, show="headings", height=10, style="Borderless.Treeview")

        for col in columns:
            table.heading(col, text=col, anchor="center")
            table.column(col, width=80, anchor="center")

        stats = get_team_statistics()
        for player_id, player_stats in stats.get("player_stats", {}).items():
            table.insert("", "end", values=(
                player_id,
                f"{player_stats.get('avg_speed', 0):.1f} km/h",
                player_stats.get('num_ball_controls', 0)
            ))

        # Configure style
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Borderless.Treeview",
            background="#2E236C",
            fieldbackground="#2E236C",
            foreground="white",
            borderwidth=0,
            highlightthickness=0
        )
        style.configure(
            "Borderless.Treeview.Heading",
            background="#2E236C",
            fieldbackground="#2E236C",
            foreground="white",
            borderwidth=0,
            relief="flat"
        )
        style.layout("Borderless.Treeview", [
            ('Borderless.Treeview.treearea', {'sticky': 'nswe'})
        ])
        style.map("Borderless.Treeview", background=[
                  ("selected", "#6B5FBF")])

        table.place(x=366, y=259, width=252, height=288)
        return table

    def _create_save_button(self):
        # Load Save Button Image
        self.save_button_image = PhotoImage(
            file=relative_to_assets("save.png"))
        self.canvas.create_image = self.canvas.create_image  # Placeholder if needed

        # Create Save Button
        save_button = Button(
            self.canvas,
            image=self.save_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_statistics,
            relief="flat",
            bg='#FFFFFF',
            activebackground='#FFFFFF'
        )
        save_button.place(
            x=761.0,
            y=572.0,
            width=163.0,
            height=36.0
        )
        self.canvas.save_button_image = self.save_button_image

    def save_statistics(self):
        stats = get_team_statistics()
        if not stats or (stats[1]["total_distance"] == 0 and stats[2]["total_distance"] == 0):
            messagebox.showerror(
                "Error", "Please run the analysis first before saving statistics!")
            return

        # Get Video Name
        if video_path:
            video_name = os.path.splitext(
                os.path.basename(video_path))[0]
        else:
            video_name = "match"

        # Default Filename
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"match_statistics_{current_time}_{video_name}.xlsx"

        # Save Dialog
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension='.xlsx',
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    # Team Statistics Sheet
                    team_data = {
                        'Metric': ['Possession (%)', 'Average Speed (km/h)',
                                   'Total Distance (m)', 'Ball Controls'],
                        'Team 1': [
                            round(stats[1]['possession'], 1),
                            round(stats[1]['avg_speed'], 1),
                            round(stats[1]['total_distance'], 1),
                            int(stats[1]['num_ball_controls'])
                        ],
                        'Team 2': [
                            round(stats[2]['possession'], 1),
                            round(stats[2]['avg_speed'], 1),
                            round(stats[2]['total_distance'], 1),
                            int(stats[2]['num_ball_controls'])
                        ]
                    }
                    team_df = pd.DataFrame(team_data)
                    team_df.to_excel(
                        writer, sheet_name='Team Statistics', index=False)

                    # Player Statistics Sheet
                    player_data = []
                    for player_id, player_stats in stats.get("player_stats", {}).items():
                        player_data.append({
                            'Player ID': player_id,
                            'Team': f"Team {player_stats.get('team', 'N/A')}",
                            'Average Speed (km/h)': round(
                                player_stats.get('avg_speed', 0), 1),
                            'Ball Controls': int(
                                player_stats.get('num_ball_controls', 0)),
                            'Distance (m)': round(
                                player_stats.get('total_distance', 0), 1)
                        })

                    player_df = pd.DataFrame(player_data)
                    player_df = player_df.sort_values(['Team', 'Player ID'])
                    player_df.to_excel(
                        writer, sheet_name='Player Statistics', index=False)

                    # Top Players Statistics Sheet
                    top_players_data = self._get_top_players_data(player_df)
                    top_players_df = pd.DataFrame(top_players_data)
                    team_rankings_df = self._get_team_rankings(player_df)

                    # Write to Excel
                    top_players_df.to_excel(
                        writer, sheet_name='Top Statistics', startrow=0, index=False)
                    team_rankings_df.to_excel(
                        writer, sheet_name='Top Statistics', startrow=len(top_players_df) + 3, index=False)

                    # Auto-adjust columns
                    worksheet = writer.sheets['Top Statistics']
                    for column in worksheet.columns:
                        max_length = 0
                        column = [cell for cell in column]
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[
                            column[0].column_letter].width = adjusted_width

                messagebox.showinfo(
                    "Success", f"Statistics successfully saved at:\n{file_path}")

            except Exception as e:
                messagebox.showerror(
                    "Error", f"An error occurred while saving the file:\n{str(e)}")

    def _get_top_players_data(self, player_df: pd.DataFrame) -> list:
        top_players_data = []

        # Top Speed
        top_speed_player = player_df.loc[player_df['Average Speed (km/h)'].idxmax()]
        top_players_data.append({
            'Category': 'Highest Average Speed',
            'Player ID': top_speed_player['Player ID'],
            'Team': top_speed_player['Team'],
            'Value': f"{top_speed_player['Average Speed (km/h)']} km/h"
        })

        # Top Distance
        top_distance_player = player_df.loc[player_df['Distance (m)'].idxmax()]
        top_players_data.append({
            'Category': 'Longest Distance',
            'Player ID': top_distance_player['Player ID'],
            'Team': top_distance_player['Team'],
            'Value': f"{top_distance_player['Distance (m)']} m"
        })

        # Most Ball Controls
        top_controls_player = player_df.loc[player_df['Ball Controls'].idxmax()]
        top_players_data.append({
            'Category': 'Most Ball Controls',
            'Player ID': top_controls_player['Player ID'],
            'Team': top_controls_player['Team'],
            'Value': f"{int(top_controls_player['Ball Controls'])} times"
        })

        return top_players_data

    def _get_team_rankings(self, player_df: pd.DataFrame) -> pd.DataFrame:
        team_rankings_data = []

        # Average Team Speed
        team_speeds = player_df.groupby('Team')['Average Speed (km/h)'].mean()
        fastest_team = team_speeds.idxmax()
        team_rankings_data.append({
            'Category': 'Fastest Team (Avg)',
            'Team': fastest_team,
            'Value': f"{round(team_speeds[fastest_team], 1)} km/h"
        })

        # Total Team Distance
        team_distances = player_df.groupby('Team')['Distance (m)'].sum()
        highest_distance_team = team_distances.idxmax()
        team_rankings_data.append({
            'Category': 'Highest Distance Team',
            'Team': highest_distance_team,
            'Value': f"{round(team_distances[highest_distance_team], 1)} m"
        })

        # Total Team Ball Controls
        team_controls = player_df.groupby('Team')['Ball Controls'].sum()
        most_controls_team = team_controls.idxmax()
        team_rankings_data.append({
            'Category': 'Most Ball Controls Team',
            'Team': most_controls_team,
            'Value': f"{int(team_controls[most_controls_team])} times"
        })

        return pd.DataFrame(team_rankings_data)

    def cleanup(self):
        plt.close('all')  # Close all figures

        if hasattr(self.canvas, 'chart_canvas'):
            self.canvas.chart_canvas.get_tk_widget().destroy()

        if hasattr(self.canvas, 'radar_chart_canvas'):
            self.canvas.radar_chart_canvas.get_tk_widget().destroy()

        self.canvas.destroy()


def Statistics(parent):
    gui = StatisticsGUI(parent)
    return gui.canvas
