from pathlib import Path
import csv
from datetime import datetime

# ----- PATH SETUP
SRC_ROOT = Path(__file__).resolve().parents[1]

LOG_DIR = SRC_ROOT / "monitoring" / "logs"
LOG_FILE = LOG_DIR / "inference_log.csv"

def initialize_log():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not LOG_FILE.exists():
        with LOG_FILE.open(mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "image", "label", "latency_ms"])
        print(f"Created log file: {LOG_FILE}")

def log_inference(image_path, result):
    with LOG_FILE.open(mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            image_path,
            result.get("label", ""),
            result.get("latency_ms", 0)
        ])
    print(f"Logged result to: {LOG_FILE}")
