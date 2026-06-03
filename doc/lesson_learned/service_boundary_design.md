# Service Boundary Design in EdgeVision AIoT System

## Background

The original prototype started as a simple single-node AI inference pipeline:

```text
Webcam
¡÷ AI inference
¡÷ Result display
```

All functionality existed within a single runtime process.

As the project evolved toward AIoT system engineering, additional responsibilities emerged:

* communication
* monitoring
* logging
* dashboard visualization
* hardware action routing
* deployment portability

This required defining explicit service boundaries.

---

# What is a Service Boundary?

A service boundary defines:

* what a module owns
* what data enters/leaves
* how components communicate
* which runtime dependencies are isolated

Good boundaries reduce coupling and improve scalability.

---

# Initial Monolithic Design

Initially:

```text
frame_to_inference.py
```

handled everything:

* image loading
* inference
* logging
* MQTT publishing
* GPIO action logic

This worked for prototyping, but caused:

* tight coupling
* poor maintainability
* deployment rigidity
* difficult debugging
* weak scalability

---

# Modular Boundary Design

The system was redesigned into separate functional domains.

---

## AI Engine

```text
ai_engine/
```

Responsibilities:

* model loading
* inference execution
* prediction generation

Output:

```json
{
  "label": "cat",
  "latency_ms": 12.3
}
```

The AI engine should not manage dashboards or hardware actions directly.

---

## Communication Layer

```text
communication/
```

Responsibilities:

* MQTT publishing
* MQTT subscription
* network message transport

The communication layer should not understand model internals.

It only transports structured messages.

---

## Monitoring Layer

```text
monitoring/
```

Responsibilities:

* logging
* inference statistics
* runtime traceability

This enables observability.

---

## Action Layer

```text
action_layer/
```

Responsibilities:

* GPIO control
* event routing
* physical device actions

This layer converts AI decisions into hardware behavior.

---

## Dashboard Node

```text
dashboard_node/
```

Responsibilities:

* visualization
* remote monitoring
* UI rendering

The dashboard consumes MQTT messages but does not run inference.

---

# Why This Matters

This architecture enables:

## 1. Independent Deployment

Each service can run separately:

```text
Raspberry Pi
Jetson Nano
Remote Laptop
Cloud VM
```

---

## 2. Fault Isolation

Dashboard crashes should not stop inference.

MQTT failures should not crash the logger.

Service boundaries improve resilience.

---

## 3. Scalability

The architecture now supports:

* multiple AI nodes
* remote dashboards
* distributed monitoring
* asynchronous communication

---

## 4. Hardware Portability

Inference and GPIO become separable concerns.

This is critical because:

* development PC
* Raspberry Pi
* Jetson
* edge devices

all have different hardware capabilities.

---

# Docker as Boundary Enforcement

Containerization made the service boundaries explicit.

Each container became:

* an isolated runtime
* with explicit dependencies
* explicit environment variables
* explicit communication interfaces

This revealed hidden assumptions that previously existed in the monolithic version.

Examples included:

* import path assumptions
* filesystem assumptions
* localhost networking assumptions

---

# Key Engineering Insight

The major evolution was not merely:

```text
single-node ¡÷ Docker
```

The true transition was:

```text
script-oriented application
¡÷ distributed system architecture
```

This is the foundation of modern AIoT engineering.

---

# Final Architecture Direction

Current system direction:

```text
Camera Node
    ¡õ
AI Inference Node
    ¡õ
MQTT Broker
    ¡õ
Dashboard / Logger / Action Nodes
```

Future Phase 3 goals:

* real-time streaming
* asynchronous runtime
* robust reconnection
* remote deployment
* multi-device orchestration
* resilience under failure conditions

The project is evolving from a local AI demo into a distributed edge AI system.
# Service Boundary Design in EdgeVision AIoT System

## Background

The original prototype started as a simple single-node AI inference pipeline:

```text
Webcam
¡÷ AI inference
¡÷ Result display
```

All functionality existed within a single runtime process.

As the project evolved toward AIoT system engineering, additional responsibilities emerged:

* communication
* monitoring
* logging
* dashboard visualization
* hardware action routing
* deployment portability

This required defining explicit service boundaries.

---

# What is a Service Boundary?

A service boundary defines:

* what a module owns
* what data enters/leaves
* how components communicate
* which runtime dependencies are isolated

Good boundaries reduce coupling and improve scalability.

---

# Initial Monolithic Design

Initially:

```text
frame_to_inference.py
```

handled everything:

* image loading
* inference
* logging
* MQTT publishing
* GPIO action logic

This worked for prototyping, but caused:

* tight coupling
* poor maintainability
* deployment rigidity
* difficult debugging
* weak scalability

---

# Modular Boundary Design

The system was redesigned into separate functional domains.

---

## AI Engine

```text
ai_engine/
```

Responsibilities:

* model loading
* inference execution
* prediction generation

Output:

```json
{
  "label": "cat",
  "latency_ms": 12.3
}
```

The AI engine should not manage dashboards or hardware actions directly.

---

## Communication Layer

```text
communication/
```

Responsibilities:

* MQTT publishing
* MQTT subscription
* network message transport

The communication layer should not understand model internals.

It only transports structured messages.

---

## Monitoring Layer

```text
monitoring/
```

Responsibilities:

* logging
* inference statistics
* runtime traceability

This enables observability.

---

## Action Layer

```text
action_layer/
```

Responsibilities:

* GPIO control
* event routing
* physical device actions

This layer converts AI decisions into hardware behavior.

---

## Dashboard Node

```text
dashboard_node/
```

Responsibilities:

* visualization
* remote monitoring
* UI rendering

The dashboard consumes MQTT messages but does not run inference.

---

# Why This Matters

This architecture enables:

## 1. Independent Deployment

Each service can run separately:

```text
Raspberry Pi
Jetson Nano
Remote Laptop
Cloud VM
```

---

## 2. Fault Isolation

Dashboard crashes should not stop inference.

MQTT failures should not crash the logger.

Service boundaries improve resilience.

---

## 3. Scalability

The architecture now supports:

* multiple AI nodes
* remote dashboards
* distributed monitoring
* asynchronous communication

---

## 4. Hardware Portability

Inference and GPIO become separable concerns.

This is critical because:

* development PC
* Raspberry Pi
* Jetson
* edge devices

all have different hardware capabilities.

---

# Docker as Boundary Enforcement

Containerization made the service boundaries explicit.

Each container became:

* an isolated runtime
* with explicit dependencies
* explicit environment variables
* explicit communication interfaces

This revealed hidden assumptions that previously existed in the monolithic version.

Examples included:

* import path assumptions
* filesystem assumptions
* localhost networking assumptions

---

# Key Engineering Insight

The major evolution was not merely:

```text
single-node ¡÷ Docker
```

The true transition was:

```text
script-oriented application
¡÷ distributed system architecture
```

This is the foundation of modern AIoT engineering.

---

# Final Architecture Direction

Current system direction:

```text
Camera Node
    ¡õ
AI Inference Node
    ¡õ
MQTT Broker
    ¡õ
Dashboard / Logger / Action Nodes
```

Future Phase 3 goals:

* real-time streaming
* asynchronous runtime
* robust reconnection
* remote deployment
* multi-device orchestration
* resilience under failure conditions

The project is evolving from a local AI demo into a distributed edge AI system.
