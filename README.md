<div align="center">

  <h1>Football Video Analyzer</h1>

</div>

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Datasets](#Datasets)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

The Football Video Analyzer is a comprehensive application designed to revolutionize football match analysis. Leveraging advanced AI and computer vision technologies, it provides in-depth insights, detailed statistics, and performance metrics for players and teams. Whether you are a coach, analyst, or passionate fan, this tool enhances decision-making and understanding of the game through data-driven analysis.

---

## Features

- **User-Friendly GUI**: Built with Tkinter, offering an intuitive interface for easy navigation between different analysis modules.
- **Video Upload & Analysis**: Upload match videos and perform thorough analysis with just a few clicks.
- **Player & Ball Tracking**: Advanced tracking of players and the ball using state-of-the-art computer vision algorithms.
- **Camera Movement Estimation**: Detect and compensate for camera movements to ensure accurate tracking data.
- **Statistical Insights**: Generate comprehensive statistics including possession, average speed, maximum speed, total distance, passes, sprints, and more.
- **Team Assignment**: Automatically assign players to teams using clustering and machine learning techniques.
- **Data Visualization**: Visual representations of player movements, team strategies, and other key metrics.
- **Exportable Reports**: Save analysis results and statistics for further review and sharing.

---

## Installation

### Prerequisites
- Python 3.8+
- Git

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/football-video-analyzer.git
    cd football-video-analyzer
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download Necessary Models**
    Ensure that all pre-trained models and assets are downloaded and placed in their respective directories as specified in the project structure.

---

## Datasets

| Use Case                        | DataSet                                                                                                                                                          | Train Model                                                                                                                                                                                            |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Soccer Player Detection         | [![Download Dataset](https://app.roboflow.com/images/download-dataset-badge.svg)](https://universe.roboflow.com/roboflow-jvuqo/football-players-detection-3zvbc) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vietbachoc/FRP_MAS_FinalProject/blob/main/backend/notebooks/train_player_detector.ipynb) |

---

## Usage

1. **Run the Application**
    ```bash
    python app.py
    ```

2. **Navigate the GUI**
    - **Home:** Overview and options to upload videos.
    - **Analysis:** Perform video analysis and view results.
    - **Statistics:** Access detailed statistics and performance metrics.
    - **About:** Learn more about the application and its mission.

3. **Upload a Video**
    - Click on the **Upload** button.
    - Select a football match video (MP4 or AVI formats).

4. **Run Analysis**
    - After uploading, click on the **Analysis** tab.
    - Start the analysis process and wait for the results.

5. **View Statistics**
    - Navigate to the **Statistics** tab to view comprehensive match data.

---

## 🔥 demos

https://streamable.com/l2l2wd

---

## Technologies Used

### Frontend
- **Tkinter:** For building the graphical user interface.
- **Matplotlib:** For creating visualizations and plots.

### Backend
- **OpenCV:** For video processing and computer vision tasks.
- **Ultralytics YOLO:** For object detection and tracking.
- **Supervision (sv):** For managing tracking algorithms.
- **Scikit-learn:** For clustering and machine learning models.
- **UMAP:** For dimensionality reduction in team assignments.
- **PyTorch:** For deep learning model integration.
- **Pandas & NumPy:** For data manipulation and analysis.
- **Transformers (Hugging Face):** For leveraging pre-trained vision models.

### Additional Tools
- **Pillow:** For image processing.
- **Pickle:** For serializing and deserializing Python objects.

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**
    ```bash
    git checkout -b feature/YourFeature
    ```
3. **Commit Your Changes**
    ```bash
    git commit -m "Add some feature"
    ```
4. **Push to the Branch**
    ```bash
    git push origin feature/YourFeature
    ```
5. **Open a Pull Request**

Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation.

---

## Contact

For questions, suggestions, or support, please contact:

- **GitHub:** [@owf2612](https://github.com/owf2612) [@vietbachoc](https://github.com/vietbachoc)
- **Discord:** owf - easy555

---

*Enhance your football match analysis with Football Video Analyzer – where data meets the game.*
