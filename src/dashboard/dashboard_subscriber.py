from pathlib import Path
import os
import time
import json
import threading
from collections import deque

import paho.mqtt.client as mqtt

# =========================
# HEADLESS BACKEND
# =========================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =========================
# MQTT CONFIG
# =========================
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "edgevision/prediction"
HEARTBEAT_TOPIC = "edgevision/heartbeat"

# =========================
# DATA BUFFER
# =========================
MAX_POINTS = 30
latencies = deque(maxlen=MAX_POINTS)
labels = deque(maxlen=MAX_POINTS)
timestamps = deque(maxlen=MAX_POINTS)
last_heartbeat_time = None

# =========================
# MQTT CALLBACKS
# =========================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
        client.subscribe(HEARTBEAT_TOPIC)
    else:
        print(f"MQTT connection failed: {rc}")

def on_message(client, userdata, msg):
    global last_heartbeat_time
    try:
        if msg.topic == HEARTBEAT_TOPIC:
            payload = json.loads(msg.payload.decode())
            last_heartbeat_time = time.time()
            print("[Heartbeat] AI node alive")
            return

        payload = json.loads(msg.payload.decode())
        label = payload.get("label", "unknown")
        latency = payload.get("latency_ms", 0)
        timestamp = time.strftime("%H:%M:%S")

        labels.append(label)
        latencies.append(latency)
        timestamps.append(timestamp)

        print(f"[MQTT] {label} | {latency:.2f} ms")

    except Exception as e:
        print(f"Message parse error: {e}")

# =========================
# MQTT THREAD
# =========================
def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            print(f"Connecting to broker: {MQTT_BROKER}")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception:
            print("MQTT broker not ready...")
            time.sleep(3)

    client.loop_forever()

# =========================
# DASHBOARD PLOT
# =========================
fig, ax = plt.subplots(figsize=(10, 5))

def update(frame):
    global last_heartbeat_time
    if last_heartbeat_time:
        elapsed = (time.time() - last_heartbeat_time)
        status = ("ONLINE" if elapsed < 20 else "OFFLINE")
    else:
        status = "UNKNOWN"

    ax.clear()
    if len(latencies) > 0:
        ax.plot(list(latencies))

    ax.set_title("Inference Latency")
    ax.set_xlabel("Frame Index")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True)
    ax.text(0.02, 0.95, f"AI Node: {status}", transform=ax.transAxes)

    # ----- Save image periodically -----
    SRC_ROOT = Path(__file__).resolve().parents[1]  # src/
    DASHBOARD_OUTPUT = SRC_ROOT / "monitoring" / "dashboard" / "dashboard_latest.png"
    DASHBOARD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(DASHBOARD_OUTPUT)
    print(f"Dashboard updated: {DASHBOARD_OUTPUT}")

# =========================
# MAIN
# =========================
def main():
    print("\nStarting dashboard node...\n")

    mqtt_thread = threading.Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()

    while True:
        update(None)
        time.sleep(2)

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    main()
