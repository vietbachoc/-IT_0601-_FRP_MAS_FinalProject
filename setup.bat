@echo off

:: Set the directory where the script is located
set DIR=%~dp0

:: Remove trailing backslash (if any)
set DIR=%DIR:~0,-1%

:: Check if 'backend\models' directory exists and create it if not
if not exist "%DIR%\backend\models" (
    mkdir "%DIR%\backend\models"
) else (
    echo 'backend\models' directory already exists.
)

:: Check if 'backend\stubs' directory exists and create it if not
if not exist "%DIR%\backend\stubs" (
    mkdir "%DIR%\backend\stubs"
) else (
    echo 'backend\stubs' directory already exists.
)

:: Check if 'videos' directory exists and create it if not
if not exist "%DIR%\videos" (
    mkdir "%DIR%\videos"
) else (
    echo 'videos' directory already exists.
)

:: Download models into 'backend\models'
echo Downloading football-ball-detection.pt...
gdown --output "%DIR%\backend\models\football-ball-detection.pt" "https://drive.google.com/uc?id=1kulJgSLBrZdKLsm-b-q_EOCAYrtOyUO_"
echo Downloading football-player-detection.pt...
gdown --output "%DIR%\backend\models\football-player-detection.pt" "https://drive.google.com/uc?id=1-g2ijN-XP9YB1mqkfysB9MhoFzruZ9Hk"
echo Downloading football-pitch-detection.pt...
gdown --output "%DIR%\backend\models\football-pitch-detection.pt" "https://drive.google.com/uc?id=1bi807YZ6s_zyCWsSnQgiMOGiU_KzvkaQ"

:: Download videos into 'videos'
echo Downloading 0bfacc_0.mp4...
gdown --output "%DIR%\videos\0bfacc_0.mp4" "https://drive.google.com/uc?id=11gspdS21z99gZUIiRq5FyRlWc0UDMe-l"
echo Downloading 2e57b9_0.mp4...
gdown --output "%DIR%\videos\2e57b9_0.mp4" "https://drive.google.com/uc?id=19o26em2UpDY9F_Mmh8eB0tXlVJQ0mm-b"
echo Downloading 08fd33_0.mp4...
gdown --output "%DIR%\videos\08fd33_0.mp4" "https://drive.google.com/uc?id=1O5yJvdBUIEnZyBNMWMloGjxg79b18pwT"
echo Downloading 573e61_0.mp4...
gdown --output "%DIR%\videos\573e61_0.mp4" "https://drive.google.com/uc?id=1XJ8eV2Yk5kAfpVIDoCf9BRn1eHNNIDH-"
echo Downloading 121364_0.mp4...
gdown --output "%DIR%\videos\121364_0.mp4" "https://drive.google.com/uc?id=1mozkXChZK0JyP1q0gfIawnVpt7y4200Z"

echo Download complete!
pause
