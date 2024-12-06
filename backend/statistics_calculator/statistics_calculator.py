import numpy as np
from typing import Dict, List, Optional
from collections import defaultdict

class StatisticsCalculator:
    def __init__(self):
        self.team_stats = {
            1: {
                "avg_speed": 0,
                "max_speed": 0,
                "total_distance": 0,
                "possession": 0,
                "num_ball_controls": 0,
                "player_count": 0,
                "active_time": 0,
                "passes": 0,
                "sprints": 0
            },
            2: {
                "avg_speed": 0,
                "max_speed": 0,
                "total_distance": 0,
                "possession": 0,
                "num_ball_controls": 0,
                "player_count": 0,
                "active_time": 0,
                "passes": 0,
                "sprints": 0
            }
        }
        
        self.player_stats = {}
        self.SPRINT_THRESHOLD = 20.0  # km/h
        self.PASS_DISTANCE_THRESHOLD = 5.0  # meters
        self.MIN_FRAMES_THRESHOLD = 10  # Minimum number of frames required for valid calculation
        self.MIN_BALL_CONTROL_FRAMES = 5  # Minimum number of frames to count as ball control
        self.frame_rate = 24  # frames per second

    def calculate_statistics(self, tracks: Dict, team_ball_control: np.ndarray) -> None:
        """Calculate all statistics from tracking data"""
        self._initialize_player_stats(tracks)
        self._calculate_player_stats(tracks)
        self._calculate_passes(tracks)
        self._remove_invalid_players()
        self._calculate_team_stats(tracks, team_ball_control)
        self._calculate_percentiles()
        
        # Add player stats to the final statistics
        self.team_stats["player_stats"] = self.player_stats

    def _initialize_player_stats(self, tracks: Dict) -> None:
        """Initialize player statistics dictionary"""
        for frame_data in tracks["players"]:
            for player_id, player_info in frame_data.items():
                if "team" in player_info and player_id not in self.player_stats:
                    self.player_stats[player_id] = {
                        "team": player_info["team"],
                        "avg_speed": 0,
                        "max_speed": 0,
                        "total_distance": 0,
                        "num_ball_controls": 0,
                        "frames_tracked": 0,
                        "speed_sum": 0,
                        "active_time": 0,
                        "passes": 0,
                        "sprints": 0,
                        "sprint_duration": 0,
                        "possession_time": 0,
                        "speed_percentile": 0,
                        "distance_percentile": 0,
                        "last_position": None,
                        "in_sprint": False,
                        "ball_control_frames": 0
                    }

    def _calculate_player_stats(self, tracks: Dict) -> None:
        """Calculate player-level statistics"""
        for frame_num, frame_data in enumerate(tracks["players"]):
            for player_id, player_info in frame_data.items():
                if player_id not in self.player_stats:
                    continue

                stats = self.player_stats[player_id]
                
                # Speed and distance calculations
                if "speed" in player_info:
                    speed = player_info["speed"]
                    stats["speed_sum"] += speed
                    stats["max_speed"] = max(stats["max_speed"], speed)
                    stats["frames_tracked"] += 1
                    
                    # Sprint detection
                    if speed >= self.SPRINT_THRESHOLD:
                        if not stats["in_sprint"]:
                            stats["sprints"] += 1
                            stats["in_sprint"] = True
                        stats["sprint_duration"] += 1
                    else:
                        stats["in_sprint"] = False

                if "distance" in player_info:
                    stats["total_distance"] = player_info["distance"]

                # Ball possession
                if player_info.get("has_ball", False):
                    stats["ball_control_frames"] += 1
                else:
                    # Check if the player had control for enough frames
                    if stats["ball_control_frames"] >= self.MIN_BALL_CONTROL_FRAMES:
                        stats["num_ball_controls"] += 1
                    stats["ball_control_frames"] = 0

                # Track active time
                if "position_transformed" in player_info:
                    stats["active_time"] += 1

        # Calculate final statistics
        for stats in self.player_stats.values():
            if stats["frames_tracked"] > 0:
                stats["avg_speed"] = stats["speed_sum"] / stats["frames_tracked"]
                stats["active_time"] = stats["frames_tracked"] / self.frame_rate  # Convert to seconds
                
            # Clean up temporary fields
            del stats["speed_sum"]
            del stats["frames_tracked"]
            del stats["in_sprint"]
            del stats["last_position"]
            del stats["ball_control_frames"]

    def _calculate_passes(self, tracks: Dict) -> None:
        """Calculate passes based on ball possession changes"""
        last_possession = defaultdict(lambda: None)  # team -> player_id
        
        for frame_num in range(len(tracks["players"])):
            current_possessor = None
            
            # Find current ball possessor
            for player_id, player_info in tracks["players"][frame_num].items():
                if player_info.get("has_ball", False):
                    current_possessor = (player_info["team"], player_id)
                    break
            
            if current_possessor is not None:
                team, player_id = current_possessor
                last_team_possessor = last_possession[team]
                
                if last_team_possessor is not None and last_team_possessor != player_id:
                    # Pass detected within team
                    if last_team_possessor in self.player_stats:
                        self.player_stats[last_team_possessor]["passes"] += 1
                
                last_possession[team] = player_id

    def _calculate_percentiles(self) -> None:
        """Calculate percentile rankings for key statistics"""
        speeds = [p["avg_speed"] for p in self.player_stats.values()]
        distances = [p["total_distance"] for p in self.player_stats.values()]
        
        for player_id, stats in self.player_stats.items():
            stats["speed_percentile"] = int(np.percentile(speeds, 
                [speeds.index(stats["avg_speed"]) / len(speeds) * 100])[0])
            stats["distance_percentile"] = int(np.percentile(distances, 
                [distances.index(stats["total_distance"]) / len(distances) * 100])[0])

    def _remove_invalid_players(self) -> None:
        """Remove players with insufficient data"""
        valid_players = {}
        for player_id, stats in self.player_stats.items():
            # Keep player if they have significant activity
            if (stats["active_time"] >= self.MIN_FRAMES_THRESHOLD / self.frame_rate and
                (stats["avg_speed"] > 0 or 
                 stats["total_distance"] > 0 or 
                 stats["num_ball_controls"] > 0)):
                valid_players[player_id] = stats
        
        self.player_stats = valid_players

    def _calculate_team_stats(self, tracks: Dict, team_ball_control: np.ndarray) -> None:
        """Calculate team-level statistics"""
        # Calculate possession percentage
        total_frames = len(team_ball_control)
        team1_frames = np.sum(team_ball_control == 1)
        team2_frames = np.sum(team_ball_control == 2)
        valid_frames = team1_frames + team2_frames
        
        if valid_frames > 0:
            self.team_stats[1]["possession"] = (team1_frames / valid_frames) * 100
            self.team_stats[2]["possession"] = (team2_frames / valid_frames) * 100

        # Reset and aggregate team stats
        for team_id in [1, 2]:
            stats = self.team_stats[team_id]
            stats.update({
                "avg_speed": 0,
                "max_speed": 0,
                "total_distance": 0,
                "num_ball_controls": 0,
                "player_count": 0,
                "active_time": 0,
                "passes": 0,
                "sprints": 0
            })

        # Aggregate player stats to team stats
        for player_id, player_stats in self.player_stats.items():
            team_id = player_stats["team"]
            team_stats = self.team_stats[team_id]
            
            team_stats["avg_speed"] += player_stats["avg_speed"]
            team_stats["max_speed"] = max(team_stats["max_speed"], player_stats["max_speed"])
            team_stats["total_distance"] += player_stats["total_distance"]
            team_stats["num_ball_controls"] += player_stats["num_ball_controls"]
            team_stats["active_time"] += player_stats["active_time"]
            team_stats["passes"] += player_stats["passes"]
            team_stats["sprints"] += player_stats["sprints"]
            team_stats["player_count"] += 1

        # Calculate team averages
        for team_id in [1, 2]:
            if self.team_stats[team_id]["player_count"] > 0:
                self.team_stats[team_id]["avg_speed"] /= self.team_stats[team_id]["player_count"]
                self.team_stats[team_id]["active_time"] /= self.team_stats[team_id]["player_count"]

    def get_player_ranking(self, stat_name: str) -> List[tuple]:
        """Get player rankings for a specific statistic"""
        return sorted(
            [(player_id, stats[stat_name]) for player_id, stats in self.player_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )
