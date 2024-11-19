# Get the directory where the script is located
$DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Create directories if they don't exist
$directories = @("backend\models", "backend\stubs", "videos")
foreach ($dir in $directories) {
    $path = Join-Path $DIR $dir
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory
        Write-Host "Created directory: $path"
    } else {
        Write-Host "'$path' already exists."
    }
}

# Download files using gdown
$downloads = @(
    @{url = "https://drive.google.com/uc?id=1kulJgSLBrZdKLsm-b-q_EOCAYrtOyUO_"; file = "backend\models\football-ball-detection.pt"},
    @{url = "https://drive.google.com/uc?id=1-g2ijN-XP9YB1mqkfysB9MhoFzruZ9Hk"; file = "backend\models\football-player-detection.pt"},
    @{url = "https://drive.google.com/uc?id=1bi807YZ6s_zyCWsSnQgiMOGiU_KzvkaQ"; file = "backend\models\football-pitch-detection.pt"},
    @{url = "https://drive.google.com/uc?id=11gspdS21z99gZUIiRq5FyRlWc0UDMe-l"; file = "videos\0bfacc_0.mp4"},
    @{url = "https://drive.google.com/uc?id=19o26em2UpDY9F_Mmh8eB0tXlVJQ0mm-b"; file = "videos\2e57b9_0.mp4"},
    @{url = "https://drive.google.com/uc?id=1O5yJvdBUIEnZyBNMWMloGjxg79b18pwT"; file = "videos\08fd33_0.mp4"},
    @{url = "https://drive.google.com/uc?id=1XJ8eV2Yk5kAfpVIDoCf9BRn1eHNNIDH-"; file = "videos\573e61_0.mp4"},
    @{url = "https://drive.google.com/uc?id=1mozkXChZK0JyP1q0gfIawnVpt7y4200Z"; file = "videos\121364_0.mp4"}
)

foreach ($download in $downloads) {
    $url = $download.url
    $file = Join-Path $DIR $download.file
    Write-Host "Downloading $file..."
    gdown --output $file $url
}

Write-Host "Download complete!"
