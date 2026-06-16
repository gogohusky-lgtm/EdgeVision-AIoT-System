# EdgeVision-AIoT-System

A modular Edge AI + AIoT integration system designed for Raspberry Pi and Jetson platforms.

This project focuses on:
- Edge AI inference
- Embedded Linux deployment
- Sensor integration
- AIoT system architecture
- Real-time monitoring

## Goal
- Deploy AI model on edge devices
- Integrate sensors and camera input
- Build real-world AIoT system

## Hardware
- Raspberry Pi 5
- Jetson Nano
- ESP32 / Arduino series

## System Architecture
![System Architecture](architecutre/phase2_runtime_architecture.png)


# Edge AIoT System Evolution Comparison

| Phase | Achievements (Outcome) | Transformation |
|-------|-------------------------|----------------|
| **Phase 0 — Modularized Edge AI** | - Modular AI inference architecture<br>- Monitoring layer abstraction<br>- Action layer abstraction<br>- Hardware-independent design<br>- Reusable inference pipeline | From **single Python inference script** → **modular Edge AI application** |
| **Phase 1 — Containerized Edge AI** | - Dockerized deployment<br>- MQTT-based service communication<br>- Distributed runtime architecture<br>- Publish-subscribe messaging<br>- Multi-service orchestration | From **modular Edge AI application** → **distributed AIoT platform prototype** |
| **Phase 2 — Resilient Edge AI** | Stress-tested with 322-image burst workload:<br>- Complete edge runtime stabilization with 100% data integrity under multi-threaded load<br>- Fully functional blocking backpressure handling via bounded queue<br>- Deterministic, zero-data-loss graceful shutdown and workspace draining<br>- Resilient background monitoring with automatic socket restoration and telemetry heartbeats | From **distributed AIoT platform prototype demonstration** → **hardened, resilient, production-ready Edge AIoT system architecture** |



where the phase 2 runtime-heardening actions to build resilient edge AI is detailed as following:

| Stage   | Focus              | Details  |
| ------- | ------------------ |----------|
| Phase2A | Observability      | - MQTT Monitoring<br> - Heartbeat<br> - Logging<br> - Dashboard |
| Phase2B | Runtime Resilience |- Queue Architecture<br> - Producer/Consumer Thread<br> - Exception Recovery<br> - Graceful Shutdown<br> - Queue Policy/backpressure |


## Current Status

| Phase | Status |
|---------|---------|
| Phase 0 — Modularized Edge AI |  Completed |
| Phase 1 — Containerized AIoT Platform |  Completed |
| Phase 2 — Runtime Hardening |  Completed |
| Phase 3 — Edge Depolymenet |  Planned |


## Key Engineering Achievements

### AI & Edge Deployment

- Modular AI Inference Engine
- Raspberry Pi / Jetson Deployment
- Dockerized Runtime Environment

### Distributed Systems

- MQTT-based Communication
- Multi-Service Architecture
- Dashboard Monitoring

### Runtime Engineering

- Producer-Consumer Queue Architecture
- Multi-threaded Processing
- Exception Recovery
- Graceful Shutdown
- Blocking Backpressure Queue
- Burst-Traffic Stress Testing


## Repository Structure

EdgeVision-AIoT-System/
│
├── docker-compose.yml
│
├── architecture/phase2_runtime_architecture.png
│
├── docs/
│     ├── architecture/
│     ├── phases/
│     ├── debugging/
│     ├── deployment/
│     └── lessons_learned/
│
└── src/
      │
      ├── inference_core.py
      │
      ├── ai_engine/
      │      ├── Dockerfile_ai_node
      │      └── requirements_ai_node.txt      
      │
      ├── action_layer/
      │     ├── gpio_controller.py
      │     └── action_router.py
      │
      ├── camera_input/
      │     ├── captured_frames/      
      │     └── webcam_capture.py
      │
      ├── monitoring/
      │     ├── dashboard/dashboard_latest.png   
      │     └── logger.py
      │
      ├── mosquitto/
      │     └── mosquqitto.conf
      │      
      ├── communication/
      │     ├── mqtt_subscriber.py 
      │     └── mqtt_publisher.py
      │      
      ├── dashboard_node/
      │     ├── Dockerfile_dashboard_node
      │     ├── requirement_dashboard_node.py 
      │     └── dashboard_subscriber.py
      │      
      └── runtime/
            ├── monitoring/logs/inference_log.csv    
            ├── models/pet_classifier_fp16.tflite   
            ├── frame_to_inference.py
            ├── frame_queue.py
            ├── producer.py
            └── consumer.py
   
docs/
├── phases/
│   ├── phase0_modularied_edge_ai.md
│   ├── phase1_containerization.md
│   └── phase2_robustness.md
│
├── architecture/
│   ├── initial_architecture.md
│   ├── modularization.md
│   ├── multi_node_design.md
│   └── communication_flow.md
│
├── debugging/
│   ├── queue_draining_and_duplicate_enqueue_analysis.md
│   ├── mqtt_connection_refused.md
│   ├── tensorflow_container_warning.md
│   ├── python_package_resolution.md
│
└── lessons_learned/
    ├── why_package_structure_matters.md
    ├── docker_context_vs_copy.md
    ├── service_boundary_design.md
    ├── threaded runtime introduced race condition.md
    └── runtime architecture upgrade.md
