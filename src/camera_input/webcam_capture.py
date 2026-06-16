import cv2
from pathlib import Path
import time

SRC_ROOT = Path(__file__).resolve().parents[1]

SAVE_DIR = (SRC_ROOT / "camera_input" / "captured_frames")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

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
        filename = SAVE_DIR / f"frame_{frame_count}.jpg"
        cv2.imwrite(str(filename), frame)
        print(f"Saved: {filename}")
        frame_count += 1
        last_capture = now
