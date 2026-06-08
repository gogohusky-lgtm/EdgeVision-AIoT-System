# Changelog

## Phase 2A

Added:
- MQTT Publisher
- MQTT Subscriber
- Mosquitto Broker
- Heartbeat Monitoring
- Dashboard PNG Export
- CSV Logging

Validated:
- Multi-container Docker deployment
- AI Node ? MQTT Broker ? Dashboard Node communication

## Phase2B

introduces a producer-consumer runtime architecture.

Goals:
- Decouple frame ingestion from inference execution
- Prevent burst traffic from blocking inference
- Improve runtime robustness
- Enable future scaling to multi-camera sources