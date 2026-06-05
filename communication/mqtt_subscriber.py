import os
import paho.mqtt.client as mqtt

BROKER = os.getenv(
    "MQTT_BROKER",
    "localhost"
)

PORT = 1883

TOPIC = "edgevision/prediction"


# =========================
# CALLBACKS
# =========================

def on_connect(
    client,
    userdata,
    flags,
    rc
):

    if rc == 0:

        print(
            "Connected to broker."
        )

        client.subscribe(TOPIC)

        print(
            f"Subscribed: {TOPIC}"
        )

    else:

        print(
            f"Connection failed: {rc}"
        )


def on_disconnect(
    client,
    userdata,
    rc
):

    print(
        f"Disconnected "
        f"(rc={rc})"
    )


def on_message(
    client,
    userdata,
    msg
):

    payload = msg.payload.decode()

    print("\n[MQTT RECEIVED]")

    print(
        f"Topic: {msg.topic}"
    )

    print(
        f"Message: {payload}"
    )


# =========================
# MAIN
# =========================

client = mqtt.Client()

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_message = on_message

client.reconnect_delay_set(
    min_delay=1,
    max_delay=60
)

client.connect(
    BROKER,
    PORT,
    keepalive=60
)

print(
    "Starting MQTT subscriber..."
)

client.loop_forever()