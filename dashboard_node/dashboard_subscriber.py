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
from matplotlib.animation import FuncAnimation

# =========================
# MQTT CONFIG
# =========================

MQTT_BROKER = os.getenv(
    "MQTT_BROKER",
    "localhost"
)

MQTT_PORT = 1883

MQTT_TOPIC = "edgevision/prediction"

# =========================
# DATA BUFFER
# =========================

MAX_POINTS = 30

latencies = deque(maxlen=MAX_POINTS)

labels = deque(maxlen=MAX_POINTS)

timestamps = deque(maxlen=MAX_POINTS)

# =========================
# MQTT CALLBACKS
# =========================

def on_connect(
    client,
    userdata,
    flags,
    rc
):

    if rc == 0:

        print(
            "Connected to MQTT broker."
        )

        client.subscribe(
            MQTT_TOPIC
        )

    else:

        print(
            f"MQTT connection failed: {rc}"
        )


def on_message(
    client,
    userdata,
    msg
):

    try:

        payload = json.loads(
            msg.payload.decode()
        )

        label = payload.get(
            "label",
            "unknown"
        )

        latency = payload.get(
            "latency_ms",
            0
        )

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        labels.append(label)

        latencies.append(latency)

        timestamps.append(timestamp)

        print(
            f"[MQTT] "
            f"{label} | "
            f"{latency:.2f} ms"
        )

    except Exception as e:

        print(
            f"Message parse error: {e}"
        )

# =========================
# MQTT THREAD
# =========================

def mqtt_loop():

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    # =========================
    # Retry until broker ready
    # =========================

    while True:

        try:

            print(
                f"Connecting to broker: "
                f"{MQTT_BROKER}"
            )

            client.connect(
                MQTT_BROKER,
                MQTT_PORT,
                60
            )

            break

        except Exception as e:

            print(
                "MQTT broker not ready..."
            )

            time.sleep(3)

    client.loop_forever()

# =========================
# DASHBOARD PLOT
# =========================

fig, ax = plt.subplots(
    figsize=(10, 5)
)

def update(frame):

    ax.clear()

    ax.plot(
        list(latencies)
    )

    ax.set_title(
        "Inference Latency"
    )

    ax.set_xlabel(
        "Frame Index"
    )

    ax.set_ylabel(
        "Latency (ms)"
    )

    ax.grid(True)

    # =========================
    # Save image periodically
    # =========================

    plt.tight_layout()

    plt.savefig(
        "dashboard_latest.png"
    )

# =========================
# MAIN
# =========================

def main():

    print(
        "\nStarting dashboard node...\n"
    )

    # =========================
    # MQTT Thread
    # =========================

    mqtt_thread = threading.Thread(
        target=mqtt_loop,
        daemon=True
    )

    mqtt_thread.start()

    # =========================
    # Animation
    # =========================

    ani = FuncAnimation(
        fig,
        update,
        interval=2000,
        cache_frame_data=False
    )

    # =========================
    # Headless loop
    # =========================

    while True:

        time.sleep(1)

# =========================
# ENTRY
# =========================

if __name__ == "__main__":

    main()