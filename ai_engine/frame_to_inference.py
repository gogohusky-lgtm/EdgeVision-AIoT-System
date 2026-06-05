import os
import sys
import time

# =========================
# PATH SETUP
# =========================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

sys.path.append(PROJECT_ROOT)

# =========================
# IMPORTS
# =========================

from inference_core import PetClassifier

from monitoring.logger import (
    initialize_log,
    log_inference
)

from action_layer.action_router import (
    ActionRouter
)

from communication.mqtt_publisher import (
    MQTTPublisher
)

# =========================
# CONFIG
# =========================

FRAME_DIR = "camera_input/captured_frames"

MODEL_PATH = "ai_engine/models/pet_classifier_fp16.tflite"

POLLING_INTERVAL = 1

HEARTBEAT_INTERVAL=10

# =========================
# MAIN
# =========================

def main():

    print("\nStarting EdgeVision frame consumer...\n")

    # =========================
    # Monitoring Layer
    # =========================

    initialize_log()

    # =========================
    # AI Engine
    # =========================

    classifier = PetClassifier(
        MODEL_PATH
    )

    # =========================
    # Action Layer
    # =========================

    router = ActionRouter()

    # =========================
    # Communication Layer
    # =========================

    mqtt_pub = MQTTPublisher()

    print("System initialized.\n")

    try:
    
        
        last_heartbeat = time.time()

        while True:

        
            current_time = time.time()

            if current_time - last_heartbeat > HEARTBEAT_INTERVAL:

                mqtt_pub.publish_heartbeat()

                last_heartbeat = current_time


            files = os.listdir(
                FRAME_DIR
            )

            jpg_files = [

                f for f in files

                if f.endswith(".jpg")

            ]

            # =========================
            # No frame available
            # =========================

            if len(jpg_files) == 0:

                time.sleep(
                    POLLING_INTERVAL
                )

                continue

            # =========================
            # Process each frame
            # =========================

            for file in jpg_files:

                filepath = os.path.join(
                    FRAME_DIR,
                    file
                )

                print(
                    f"\nProcessing: {filepath}"
                )

                # =========================
                # AI inference
                # =========================

                result = classifier.infer_image_path(
                    filepath
                )

                print(
                    f"Prediction: "
                    f"{result['label']} "
                    f"| Latency: "
                    f"{result['latency_ms']:.2f} ms"
                )

                # =========================
                # Monitoring Layer
                # =========================

                log_inference(
                    filepath,
                    result
                )

                print(
                    "Logged inference result."
                )

                # =========================
                # Action Layer
                # =========================

                router.handle_prediction(
                    result["label"]
                )

                # =========================
                # Communication Layer
                # =========================

                mqtt_pub.publish_prediction(
                    result
                )

                # =========================
                # Cleanup processed frame
                # =========================

                os.remove(
                    filepath
                )

                print(
                    f"Removed: {filepath}"
                )

            # =========================
            # Polling interval
            # =========================

            time.sleep(
                POLLING_INTERVAL
            )

    # =========================
    # Graceful Shutdown
    # =========================

    except KeyboardInterrupt:

        print(
            "\nShutting down system..."
        )

        router.shutdown()

        print(
            "System stopped."
        )


# =========================
# ENTRY
# =========================

if __name__ == "__main__":

    main()