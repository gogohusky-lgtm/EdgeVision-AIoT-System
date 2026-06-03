# Phase 1 ¡X Containerized Multi-Node AIoT Pipeline

## Objective

Transform the single-node AI application into a distributed AIoT system.

This phase introduced:

- Docker
- MQTT
- multi-service orchestration
- distributed communication
- containerized runtime

---

# System Architecture

Multi-node architecture:

Camera/Input Node
        ¡õ
AI Inference Node
        ¡õ MQTT
Dashboard Node

Broker:
Mosquitto MQTT

---

# Key Components

## AI Node

Responsibilities:

- frame polling
- inference execution
- logging
- MQTT publishing

Containerized using Docker.

---

## Dashboard Node

Responsibilities:

- MQTT subscription
- visualization
- runtime monitoring

Executed independently from inference node.

---

## MQTT Broker

Responsibilities:

- message routing
- decoupled communication
- service interoperability

Implemented using Eclipse Mosquitto.

---

# Key Engineering Challenges

## 1. Python package resolution inside containers

Encountered:

- ModuleNotFoundError
- incorrect COPY scope
- broken package imports

Resolved by:

- proper package structure
- __init__.py
- correct Docker build context

---

## 2. Docker context vs runtime path

Learned distinction between:

- host filesystem
- container filesystem
- build context
- runtime working directory

Critical insight for containerized systems.

---

## 3. MQTT service startup timing

Observed:

ConnectionRefusedError

Cause:

services starting before broker fully initialized.

Solution:

- retry loops
- delayed connection logic
- runtime resilience patterns

---

## 4. TensorFlow container warnings

Observed warnings:

- libcudart.so
- TensorRT libraries

Determined to be:

non-fatal CPU-only warnings.

Important distinction between:

- warning
- runtime failure

---

# Key Engineering Lessons

## 1. Deployment is a separate engineering domain

A working Python application is not yet a deployable system.

Deployment introduces:

- networking
- filesystem isolation
- dependency management
- service orchestration

---

## 2. Service boundaries matter

System evolved from:

"multiple Python scripts"

into:

"distributed services communicating over protocols"

This is a major architectural transition.

---

## 3. Containers expose architecture weaknesses

Many hidden assumptions failed inside Docker:

- relative paths
- implicit imports
- local filesystem assumptions

Containerization forced cleaner architecture.

---

# Outcome

Successfully achieved:

- containerized AI inference node
- MQTT-based communication
- distributed dashboard subscriber
- Docker Compose orchestration
- modular multi-service runtime

This phase transformed the project from:

local AI demo

into:

distributed AIoT system prototype.