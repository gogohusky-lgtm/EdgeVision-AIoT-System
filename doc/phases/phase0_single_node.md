# Phase 0 ¡X Single Node AI Inference System

## Objective

Build a local edge AI inference pipeline with modularized architecture.

This phase focused on:

- AI inference pipeline
- modular architecture
- data flow validation
- local monitoring
- GPIO action abstraction

---

# System Architecture

Single-node architecture:

Camera/Input
    ¡õ
Inference Engine
    ¡õ
Monitoring
    ¡õ
Action Layer

All components executed locally on one machine.

---

# Key Components

## AI Engine

Responsible for:

- loading TFLite model
- preprocessing image
- running inference
- returning prediction + latency

Main files:

- inference_core.py
- frame_to_inference.py

---

## Monitoring Layer

Responsible for:

- inference logging
- CSV generation
- runtime visibility

Main files:

- logger.py

---

## Action Layer

Responsible for:

- GPIO abstraction
- prediction-triggered actions

Main files:

- gpio_controller.py
- action_router.py

---

# Key Engineering Lessons

## 1. Modularization matters

Originally implemented as one large inference script.

Refactored into:

- inference
- monitoring
- action
- communication

This significantly improved maintainability.

---

## 2. Dataflow clarity is critical

Validated full inference flow:

image
¡÷ inference
¡÷ logging
¡÷ action

This became the foundation for future distributed deployment.

---

## 3. Hardware abstraction

GPIO logic separated from inference logic.

This enabled:

- desktop testing
- Raspberry Pi deployment
- container compatibility

---

# Outcome

Successfully created:

- reusable AI inference pipeline
- modular edge AI architecture
- system-oriented codebase

This phase established the foundation for distributed AIoT deployment.