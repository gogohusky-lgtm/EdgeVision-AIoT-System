# modularization.md

# Modularization Strategy

## Objective

Refactor the original inference prototype into a modular AIoT-oriented architecture.

The goal was to separate responsibilities into independent system layers.

---

# Motivation

Initially, the system was implemented as a single inference-oriented script.

This created several issues:

* difficult maintenance
* mixed responsibilities
* limited scalability
* deployment complexity

To improve maintainability and deployment readiness, the system was modularized.

---

# Module Separation

## Camera Input Layer

Responsible for frame acquisition.

Directory:

* camera_input/

Main file:

* webcam_capture.py

---

## AI Engine Layer

Responsible for:

* preprocessing
* inference execution
* prediction generation

Directory:

* ai_engine/

Main files:

* frame_to_inference.py
* inference_core.py

---

## Communication Layer

Responsible for:

* MQTT publishing
* MQTT subscription
* inter-service communication

Directory:

* communication/

Main files:

* mqtt_publisher.py
* mqtt_subscriber.py

---

## Monitoring Layer

Responsible for:

* inference logging
* runtime monitoring
* CSV persistence

Directory:

* monitoring/

Main file:

* logger.py

---

## Dashboard Layer

Responsible for:

* visualization
* MQTT data display
* runtime observation

Directory:

* dashboard_node/

Main file:

* dashboard_subscriber.py

---

## Action Layer

Responsible for:

* GPIO abstraction
* hardware action routing

Directory:

* action_layer/

Main files:

* action_router.py
* gpio_controller.py

---

# Key Design Principles

## Separation of Concerns

Each module handles a single responsibility.

---

## Deployment Flexibility

Modules can later be distributed into:

* separate containers
* separate devices
* remote edge nodes

---

## Hardware Abstraction

GPIO and hardware-specific logic are isolated from AI inference logic.

---

# Outcome

The project evolved from:

single inference script

into:

modular AIoT system architecture.
