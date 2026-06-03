import os
import json
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv(
    "MQTT_BROKER",
    "localhost"
)

PORT = 1883

TOPIC = "edgevision/prediction"


class MQTTPublisher:

    def __init__(self):

        self.client = mqtt.Client()

        connected = False

        while not connected:

            try:

                print(
                    f"Connecting to MQTT broker: {BROKER}"
                )

                self.client.connect(
                    BROKER,
                    PORT,
                    60
                )

                connected = True

                print(
                    "MQTT connected."
                )

            except Exception as e:

                print(
                    f"MQTT connection failed: {e}"
                )

                print(
                    "Retrying in 3 seconds..."
                )

                time.sleep(3)

    def publish_prediction(
        self,
        result
    ):

        payload = json.dumps(result)

        self.client.publish(
            TOPIC,
            payload
        )

        print(
            f"Published MQTT: {payload}"
        )