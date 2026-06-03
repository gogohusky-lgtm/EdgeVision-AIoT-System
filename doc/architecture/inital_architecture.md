# initial_architecture.md

# Initial Architecture - Single Node AI Inference System

## Objective

The initial architecture focused on building a local edge AI inference pipeline capable of:

* webcam frame ingestion
* image inference
* prediction event generation
* runtime monitoring
* local action triggering

All components were executed within a single runtime environment.

---

# System Flow

Webcam
↓
Captured Frame
↓
AI Inference Engine
↓
Prediction / Event
↓
Monitoring + Logging + Action

---

# Core Components

## Camera Input

Responsible for:

* webcam frame capture
* frame storage

Main file:

* camera_input/webcam_capture.py

---

## AI Engine

Responsible for:

* image preprocessing
* TensorFlow Lite inference
* prediction generation
* latency measurement

Main files:

* ai_engine/frame_to_inference.py
* ai_engine/inference_core.py

---

## Monitoring Layer

Responsible for:

* runtime logging
* inference tracking
* CSV log generation

Main file:

* monitoring/logger.py

---

## Action Layer

Responsible for:

* GPIO abstraction
* prediction-triggered action routing

Main files:

* action_layer/action_router.py
* action_layer/gpio_controller.py

---

# Key Characteristics

## Monolithic Runtime

All modules executed locally inside one Python runtime.

Advantages:

* simple debugging
* fast iteration
* direct data flow visibility

Limitations:

* poor scalability
* tightly coupled architecture
* difficult deployment separation

---

# Evolution Direction

This architecture later evolved into:

* MQTT-based communication
* containerized deployment
* distributed multi-node services
* decoupled runtime architecture
