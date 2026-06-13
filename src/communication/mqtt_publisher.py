import os
import json
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = 1883
TOPIC = "edgevision/prediction"
HEARTBEAT_TOPIC = "edgevision/heartbeat"

# =========================
# CALLBACKS
# =========================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker.")
    else:
        print(f"Connection failed: rc={rc}")


def on_disconnect(client, userdata, rc):

    if rc != 0: print(f"Unexpected disconnect "f"(rc={rc})")

    else: print("Clean disconnect.")


def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

def publish_heartbeat(self):

    payload = {
        "node": "ai_node",
        "status": "alive",
        "timestamp": time.time()
    }

    self.client.publish(
        HEARTBEAT_TOPIC,
        json.dumps(payload),
        qos=1
    )


# =========================
# PUBLISHER CLASS
# =========================

class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client()

        # �j�w callbacks
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_publish = on_publish


        # �]�w�۰ʭ��s����
        self.client.reconnect_delay_set(min_delay=1, max_delay=60)

        connected = False
        while not connected:
            try:
                print(f"Connecting to MQTT broker: {BROKER}:{PORT}")
                self.client.connect(BROKER, PORT, keepalive=60)
                connected = True
                print("MQTT connected.")
            except Exception as e:
                print(f"MQTT connection failed: {e}")
                print("Retrying in 3 seconds...")
                time.sleep(3)

        # �Ұ� loop�A�� client �۰ʳB�z�����ƥ�
        self.client.loop_start()

    def publish_prediction(self, result):

        try:

            payload = json.dumps(result)

            ret = self.client.publish(
                TOPIC,
                payload,
                qos=1
            )

            ret.wait_for_publish()

            if ret.rc != mqtt.MQTT_ERR_SUCCESS:

                print(
                    f"Publish failed: {ret.rc}"
                )

            else:

                print(
                    f"[MQTT Published] {payload}"
                )

        except Exception as e:

            print(
                f"Error publishing message: {e}"
            )

    def publish_heartbeat(self):

        payload = {
            "node": "ai_node",
            "status": "alive",
            "timestamp": time.time()
        }

        ret = self.client.publish(
            HEARTBEAT_TOPIC,
            json.dumps(payload),
            qos=1
        )
        ret.wait_for_publish()
        print(
            f"[Heartbeat Published] {time.strftime('%H:%M:%S')}"
        )

    def disconnect(self):

        try:

            print(
                "Disconnecting MQTT..."
            )

            self.client.loop_stop()

            self.client.disconnect()

        except Exception as e:

            print(
                f"MQTT disconnect error: {e}"
            )
