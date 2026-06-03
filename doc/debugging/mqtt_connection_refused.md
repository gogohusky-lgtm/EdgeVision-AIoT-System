# MQTT Connection Refused During Container Deployment

## Symptom

After successfully building all Docker images:

```bash
docker compose build
```

containers still failed during runtime.

Typical error:

```python
ConnectionRefusedError: [Errno 111] Connection refused
```

appeared in:

* ai_node
* dashboard_node

when attempting to connect to MQTT.

---

# Initial Assumption

The first assumption was:

```text
Mosquitto broker failed to start.
```

However logs showed:

```text
mosquitto version 2.1.2 running
Opening ipv4 listen socket on port 1883
```

indicating the broker was running correctly.

---

# Root Cause

The issue was caused by incorrect MQTT host configuration.

Original code:

```python
client.connect("localhost",1883)
```

Inside Docker containers:

```text
localhost
```

means:

```text
this container itself
```

not another container.

Therefore:

```text
ai_node
```

attempted to connect to:

```text
ai_node:1883
```

instead of:

```text
mqtt_broker:1883
```

which caused the connection failure.

---

# Docker Networking Model

Docker Compose automatically creates an internal network.

Each service becomes discoverable by its service name.

Example:

```yaml
services:

  broker:
    image: eclipse-mosquitto

  ai_node:
    ...

  dashboard_node:
    ...
```

Internal DNS names become:

```text
broker
ai_node
dashboard_node
```

respectively.

---

# Correct Solution

Use environment variables:

```yaml
environment:
  - MQTT_BROKER=broker
```

and retrieve them inside Python:

```python
MQTT_BROKER = os.getenv(
    "MQTT_BROKER",
    "broker"
)
```

Connection:

```python
client.connect(
    MQTT_BROKER,
    1883,
    60
)
```

---

# Verification

Successful broker logs:

```text
New client connected from ...
```

indicated MQTT communication was established.

After correction:

* publisher connected successfully
* subscriber connected successfully
* messages were exchanged through Mosquitto

---

# Engineering Lesson

A common mistake when containerizing applications is assuming:

```text
localhost == another service
```

This is never true inside containers.

The correct mental model is:

```text
Container
    ¡õ
Docker Network
    ¡õ
Service Name Discovery
```

instead of:

```text
Container
    ¡õ
localhost
```

Understanding this distinction is fundamental when moving from single-node applications to distributed systems.
