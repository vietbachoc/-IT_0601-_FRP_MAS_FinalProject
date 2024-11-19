#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if 'backend/models' directory does not exist and then create it
if [[ ! -e $DIR/backend/models ]]; then
    mkdir -p "$DIR/backend/models"
else
    echo "'backend/models' directory already exists."
fi

# Check if 'backend/stubs' directory does not exist and then create it
if [[ ! -e $DIR/backend/stubs ]]; then
    mkdir -p "$DIR/backend/stubs"
else
    echo "'backend/stubs' directory already exists."
fi

# Check if 'videos' directory does not exist and then create it
if [[ ! -e $DIR/videos ]]; then
    mkdir "$DIR/videos"
else
    echo "'videos' directory already exists."
fi

# Download the models into 'backend/models' using curl
curl -L -o "$DIR/backend/models/football-ball-detection.pt" "https://drive.google.com/uc?id=1kulJgSLBrZdKLsm-b-q_EOCAYrtOyUO_"
curl -L -o "$DIR/backend/models/football-player-detection.pt" "https://drive.google.com/uc?id=1-g2ijN-XP9YB1mqkfysB9MhoFzruZ9Hk"
curl -L -o "$DIR/backend/models/football-pitch-detection.pt" "https://drive.google.com/uc?id=1bi807YZ6s_zyCWsSnQgiMOGiU_KzvkaQ"

# Download the videos into 'videos' using curl
curl -L -o "$DIR/videos/0bfacc_0.mp4" "https://drive.google.com/uc?id=11gspdS21z99gZUIiRq5FyRlWc0UDMe-l"
curl -L -o "$DIR/videos/2e57b9_0.mp4" "https://drive.google.com/uc?id=19o26em2UpDY9F_Mmh8eB0tXlVJQ0mm-b"
curl -L -o "$DIR/videos/08fd33_0.mp4" "https://drive.google.com/uc?id=1O5yJvdBUIEnZyBNMWMloGjxg79b18pwT"
curl -L -o "$DIR/videos/573e61_0.mp4" "https://drive.google.com/uc?id=1XJ8eV2Yk5kAfpVIDoCf9BRn1eHNNIDH-"
curl -L -o "$DIR/videos/121364_0.mp4" "https://drive.google.com/uc?id=1mozkXChZK0JyP1q0gfIawnVpt7y4200Z"

echo "Download complete!"