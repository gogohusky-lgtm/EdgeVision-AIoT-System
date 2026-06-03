import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883

TOPIC = "edgevision/prediction"


# =========================
# CALLBACK
# =========================

def on_connect(client, userdata, flags, rc):

    print(
        f"Connected to broker "
        f"(code={rc})"
    )

    client.subscribe(TOPIC)

    print(
        f"Subscribed to: {TOPIC}"
    )


def on_message(
    client,
    userdata,
    msg
):

    payload = msg.payload.decode()

    print(
        f"\n[MQTT RECEIVED]"
    )

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

client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

print("Starting MQTT subscriber...")

client.loop_forever()