#  AirTrace - Gesture Control 
#  Libraries to be Installed 
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#  1. INITIALIZE MEDIAPIPE HAND LANDMARKER 
# Load the pre-trained hand landmarker model (ensure hand_landmarker.task is in the root directory)
model_path = 'hand_landmarker.task' 
base_options = python.BaseOptions(model_asset_path=model_path)
# Configuration for 1-hand tracking with standard detection confidence
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

# 2. APPLICATION VARIABLES 
cap = cv2.VideoCapture(0) # Open default webcam
canvas = None             # Holds the persistent drawing layer
prev_x, prev_y = None, None # Stores previous point to draw continuous lines

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Mirror the frame for an intuitive drawing experience
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # Initialize the canvas with the same dimensions as the camera feed
    if canvas is None: 
        canvas = np.zeros_like(frame)

    # Define the "RESET" button area (Bottom-Right Corner)
    btn_w, btn_h = 160, 60
    rx1, ry1, rx2, ry2 = w - btn_w - 20, h - btn_h - 20, w - 20, h - 20
    
    # Convert OpenCV BGR image to MediaPipe RGB Image object
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Execute hand landmark detection
    detection_result = detector.detect(mp_image)

    if detection_result.hand_landmarks:
        landmarks = detection_result.hand_landmarks[0]
        
        # Extract coordinates for Index Tip (8) and Thumb Tip (4)
        itip, ttip = landmarks[8], landmarks[4]
        x1, y1 = int(itip.x * w), int(itip.y * h)
        x2, y2 = int(ttip.x * w), int(ttip.y * h)

        # DRAWING & BUTTON LOGIC 
        # Calculate Euclidean distance between thumb and index tips
        dist = np.hypot(x1 - x2, y1 - y2)
        pinch = dist < (0.06 * w) # Threshold for activating the "pen"
        
        # Check if index finger is inside the RESET button boundaries
        on_button = rx1 < x1 < rx2 and ry1 < y1 < ry2

        if pinch:
            if on_button:
                # Clear the drawing layer
                canvas = np.zeros_like(frame)
                prev_x, prev_y = None, None
                # Visual feedback: Fill button when pressed
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), -1)
            else:
                # Draw a line from the previous point to the current point
                if prev_x is not None:
                    # Drawing color: Green (BGR: 0, 255, 0)
                    cv2.line(canvas, (prev_x, prev_y), (x1, y1), (0, 255, 0), 8, cv2.LINE_AA)
                prev_x, prev_y = x1, y1
        else:
            # Reset tracking points when pinch is released
            prev_x, prev_y = None, None

    #  3. UI RENDERING & MERGING 
    # Render the RESET button text and border
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)
    cv2.putText(frame, "RESET", (rx1 + 35, ry1 + 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Create a mask of the drawing to overlay on the live feed
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    frame[mask > 0] = canvas[mask > 0]

    # Show the final output
    cv2.imshow("AirTrace - Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()