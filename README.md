

# AirTrace: Gesture-Controlled Spatial Sketching

**AirTrace** is a real-time computer vision application that transforms your hand into a digital paintbrush. By leveraging **Google MediaPipe’s Tasks API** and **OpenCV**, the system tracks hand landmarks with high precision, allowing users to draw in a 3D-like digital space through simple gestures.

<img width="798" height="632" alt="AirTrace" src="https://github.com/user-attachments/assets/55d68d46-1ba2-4326-8185-92f412dfecfb" />

## Features

* **Pinch-to-Draw**: Uses a natural "pinch" gesture (connecting thumb and index finger) to activate the digital ink.
* **Persistent Canvas**: Drawings are maintained on a dedicated transparent layer overlaid on the live camera feed.
* **Spatial UI**: Features an on-screen "RESET" button at the bottom-right corner for clearing the canvas.
* **High-Quality Rendering**: Uses anti-aliasing to ensure smooth, professional-looking strokes even at high speeds.
* **Optimized Performance**: Built with the MediaPipe 2026 Tasks API for low-latency tracking on modern Python environments.

---

##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NKumar-B/VisionSketch_OpenCV/AirTrace.git
cd AirTrace

```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv .venv
.\.venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe numpy

```

### 4. Download the Model File

You must download the **Hand Landmarker** model from Google and place it in the root directory:

* **Model Name**: `hand_landmarker.task`
* **Download Link**: [Google MediaPipe Model Garden](https://www.google.com/search?q=https://developers.google.com/mediapipe/solutions/vision/hand_landmarker%23models)

---

##  How to Use

1. **Run the script**: `python AirTrace<img width="798" height="632" alt="AirTrace" src="https://github.com/user-attachments/assets/c1fd0d2f-8598-4c1f-acc2-d39997aee9e4" />
.py`
2. **Drawing**: Bring your **Index Finger** and **Thumb** together (pinch) to begin drawing in green ink.
3. **Moving**: Release the pinch to move your hand without drawing.
4. **Resetting**: Pinch your fingers while hovering over the red **RESET** box in the bottom-right corner to clear the screen.
5. **Exit**: Press the **'q'** key on your keyboard to close the application.

---

##  Technical Overview

The application follows a modular computer vision pipeline:

1. **Preprocessing**: The input frame is flipped horizontally to provide a "mirror-like" intuitive experience for the user.
2. **Detection**: MediaPipe's `HandLandmarker` identifies 21 unique landmarks. We specifically track **Landmark 8** (Index Tip) and **Landmark 4** (Thumb Tip).
3. **Distance Logic**: We calculate the Euclidean distance between these two points. If the distance falls below a specific threshold (e.g., 6% of the screen width), the "pinch" is triggered.
4. **Layer Merging**: Drawing occurs on a separate black `canvas`. We create a binary mask of this canvas and use bitwise operations to overlay only the non-black pixels onto the live camera feed.

---

##  License

Distributed under the MIT License. See `LICENSE` for more information.
