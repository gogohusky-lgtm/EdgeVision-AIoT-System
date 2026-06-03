# multi_node_design.md

# Multi-Node Distributed Design

## Objective

Transform the local AI inference system into a distributed AIoT architecture.

This phase introduced:

* Docker containerization
* MQTT communication
* service separation
* distributed runtime architecture

---

# System Topology

Camera/Input Node
¡õ
AI Inference Node
¡õ MQTT
Dashboard Node

Broker:
Mosquitto MQTT

---

# Service Separation

## AI Node

Responsibilities:

* frame polling
* inference execution
* MQTT publishing
* logging
* action routing

Containerized independently.

---

## Dashboard Node

Responsibilities:

* MQTT subscription
* prediction visualization
* runtime monitoring

Executed as separate service.

---

## MQTT Broker

Responsibilities:

* message routing
* decoupled communication
* distributed synchronization

Implemented using Eclipse Mosquitto.

---

# Containerization

Added:

* Dockerfile
* docker-compose.yml

Purpose:

* reproducible runtime
* isolated dependency management
* multi-service orchestration

---

# Key Architectural Transition

The system evolved from:

single-process local application

into:

distributed service-oriented AIoT pipeline.

---

# Key Lessons

## Deployment is part of system design

Containerization exposed:

* import issues
* package structure problems
* filesystem assumptions
* runtime dependency issues

This significantly improved architecture quality.
