# Phase 2 ¡V Real-Time Robustness and Distributed Runtime

## Objective

Phase 2 extends the containerized AIoT architecture developed in Phase 1 into a more robust and real-time distributed system.

The primary goal is to move beyond simple file-based inference and create a continuously running AIoT pipeline capable of handling live data streams, communication failures, and long-running operation.

---

## Motivation

Phase 1 successfully demonstrated:

* Modular AI architecture
* MQTT communication
* Docker containerization
* Multi-node deployment
* Runtime logging

However, the system still relies on:

* Folder polling
* Manual image injection
* Limited fault tolerance
* Basic MQTT communication

To better reflect real-world AIoT deployments, additional robustness features are required.

---

## Target Features

### Live Webcam Streaming

Replace manual image placement with continuous frame acquisition.

Current:

Webcam ¡÷ Save JPG ¡÷ Folder Polling ¡÷ Inference

Target:

Webcam ¡÷ Inference ¡÷ MQTT Publish

---

### Stable MQTT Communication

Improve communication reliability by adding:

* reconnect logic
* connection health monitoring
* retry mechanisms
* graceful error handling

---

### Real-Time Dashboard

Enable continuous dashboard updates.

Dashboard should:

* receive MQTT messages continuously
* update latency metrics
* display prediction statistics
* remain active during long runtime sessions

---

### Runtime Fault Tolerance

The system should tolerate:

* temporary MQTT outages
* missing frames
* corrupted images
* node restarts

without requiring manual intervention.

---

### Multi-Device Deployment

Future deployment targets include:

* Raspberry Pi
* Jetson Nano
* Remote Linux devices

The architecture should support distributed deployment across multiple machines.

---

## Expected Outcome

After Phase 2, the system will evolve from a demonstration pipeline into a practical distributed AIoT application capable of long-running operation and real-time communication.
