import cv2
import os
import time

SAVE_DIR = "captured_frames"

os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()


frame_count = 0

capture_interval = 3
last_capture = time.time()

while True:

    ret, frame = cap.read()

    now = time.time()

    if now - last_capture > capture_interval:

        filename = os.path.join(
            SAVE_DIR,
            f"frame_{frame_count}.jpg"
        )

        cv2.imwrite(filename, frame)

        print(f"Saved: {filename}")

        frame_count += 1
        last_capture = now