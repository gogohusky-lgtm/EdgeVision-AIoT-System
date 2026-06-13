import os
import sys
import time

#   -----   PATH SETUP
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
#print(f"Current directory: {CURRENT_DIR}")
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
#print(f"Project root: {PROJECT_ROOT}")
sys.path.append(PROJECT_ROOT)

#   -----   IMPORTS

from inference_core import PetClassifier

from monitoring.logger import (
    initialize_log,
    log_inference
)

from action_layer.action_router import ActionRouter

from communication.mqtt_publisher import MQTTPublisher

#   -----   Runtime Layer (NEW)
from runtime.frame_queue import FRAME_QUEUE
from runtime.producer import FrameProducer
from runtime.consumer import FrameConsumer

#   -----   CONFIG

FRAME_DIR = os.path.join(PROJECT_ROOT, "camera_input", "captured_frames")
#print(f"Frame directory: {FRAME_DIR}")
MODEL_PATH = os.path.join(PROJECT_ROOT, "ai_engine", "models", "pet_classifier_fp16.tflite")
#print(f"Model path: {MODEL_PATH}")


POLLING_INTERVAL = 1
HEARTBEAT_INTERVAL = 10

#   -----   MAIN

def main():

    print("\nStarting EdgeVision Runtime (Phase2B Queue Architecture)\n")

    #   -----   Monitoring Layer
    initialize_log()

    #   -----   AI Engine
    classifier = PetClassifier(MODEL_PATH)

    #   -----   Action Layer
    router = ActionRouter()

    #   -----   Communication Layer
    mqtt_pub = MQTTPublisher()

    #   -----   Runtime Layer (NEW)
    producer = FrameProducer(
        FRAME_DIR,
        FRAME_QUEUE
    )

    consumer = FrameConsumer(
        FRAME_QUEUE,
        classifier,
        router,
        mqtt_pub,
        log_inference,
        producer.queued_files   # 傳入共享的 set
    )

    print("System initialized.\n")

    try:
        producer.start()
        consumer.start()
        last_heartbeat = time.time()
        
        while True:

            current_time = time.time()

            #   -----   Heartbeat
            if (current_time - last_heartbeat > HEARTBEAT_INTERVAL):
                mqtt_pub.publish_heartbeat()
                last_heartbeat = current_time

            time.sleep(1)

    #   -----   Graceful Shutdown
    except KeyboardInterrupt:

        print("\nShutting down...")

        # -------------------------
        # Stop Producer First
        # -------------------------

        print("Stopping producer...")

        producer.stop()

        producer.join()

        print("Waiting for queue tasks...")

        # -------------------------
        # Drain Queue
        # -------------------------

        FRAME_QUEUE.join()

        print("All queue tasks completed.")
        print("Queue drained.")

        # -------------------------
        # Stop Consumer
        # -------------------------

        print("Stopping consumer...")

        consumer.stop()

        consumer.join()

        # -------------------------
        # Shutdown Action Layer
        # -------------------------

        router.shutdown()

        # -------------------------
        # MQTT Disconnect
        # -------------------------

        try:

            mqtt_pub.disconnect()

        except Exception:

            pass

        print("System stopped.")

#   -----   ENTRY

if __name__ == "__main__":
    main()