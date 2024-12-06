# Global statistics storage
team_statistics = {
    1: {
        "possession": 0,
        "avg_speed": 0,
        "max_speed": 0,
        "total_distance": 0,
        "num_ball_controls": 0,
        "player_count": 0,
        "active_time": 0,
        "passes": 0,
        "sprints": 0
    },
    2: {
        "possession": 0,
        "avg_speed": 0,
        "max_speed": 0,
        "total_distance": 0,
        "num_ball_controls": 0,
        "player_count": 0,
        "active_time": 0,
        "passes": 0,
        "sprints": 0
    },
    "player_stats": {}
}

def update_team_statistics(stats):
    global team_statistics
    team_statistics = stats

def get_team_statistics():
    return team_statistics 