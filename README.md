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
camera_input
      ¢x
      ¡¿
ai_node
 ¢u¢w AI Engine
 ¢u¢w Monitoring Layer
 ¢u¢w Action Layer
 ¢|¢w MQTT Publisher
      ¢x
      ¡¿
mqtt_broker
      ¢x
      ¡¿
dashboard_node
 ¢u¢w MQTT Subscriber
 ¢|¢w Dashboard PNG

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