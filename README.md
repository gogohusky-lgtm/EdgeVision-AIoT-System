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
Camera Input
      ¡õ
Producer
      ¡õ
Frame Queue
      ¡õ
Consumer
      ¡õ
Inference Engine
      ¡õ
Action Layer
      ¡õ
MQTT
      ¡õ
Dashboard

## Current Status

Phase 1 Completed
- AI inference pipeline
- GPIO action routing
- Docker deployment

Phase 2A Completed
- MQTT communication
- Heartbeat monitoring
- CSV logging
- Dashboard generation

Phase2B-Queue Completed
Producer ¡÷ Queue ¡÷ Consumer

- Introduced producer-consumer runtime architecture
- Added bounded frame queue buffering
- Decoupled frame ingestion from inference processing
- Improved robustness for burst frame arrivals

Next:
- Frame Queue
- System robustness
- Dashboard metrics


## Current Modules

### AI Engine
- TensorRT inference
- Edge AI benchmarking
- Jetson / Raspberry Pi deployment

### IoT Layer
- RFID access control
- Environment sensor monitoring

### Deployment
- Dockerized AI services
- Linux automation scripts

## Repository Structure

ai_engine/
action_layer/
communication/
dashboard_node/
monitoring/
camera_input/
mosquitto/
docs/