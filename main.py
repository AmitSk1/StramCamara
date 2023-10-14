import cv2
import numpy as np
from PIL import ImageGrab

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture camara_frame-by-camara_frame
    ret, camara_frame = cap.read()

    if not ret:
        print("Error: Failed to capture camara_frame.")
        break

    # Display the camara_frame

    # screen_frame = np.array(ImageGrab.grab(bbox=(0, 0, 600, 600)))
    # cv2.imshow('Screen Stream', screen_frame)
    cv2.imshow('Camera Stream', camara_frame)

    # Press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
