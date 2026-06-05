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

- Introduced producer-consumer runtime architecture
- Added bounded frame queue buffering
- Decoupled frame ingestion from inference processing
- Improved robustness for burst frame arrivals

Validated:
Phase2B-Queue
Producer ¡÷ Queue ¡÷ Consumer