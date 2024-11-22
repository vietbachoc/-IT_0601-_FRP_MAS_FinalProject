from typing import Dict

# Model constants
SIGLIP_MODEL_NAME = "google/siglip-base-patch16-224"
BATCH_SIZE = 16
IMAGE_SIZE = 224

# UMAP parameters
UMAP_CONFIG = {
    "n_components": 3,
    "random_state": None,
    "n_jobs": -1,
    "min_dist": 0.1,
    "n_neighbors": 15
}

# Team colors
TEAM_COLORS: Dict[int, str] = {
    1: "#ff1493",  # Deep Pink
    2: "#00bfff"   # Deep Sky Blue
}

# Minimum players needed for team classification
MIN_PLAYERS = 2 