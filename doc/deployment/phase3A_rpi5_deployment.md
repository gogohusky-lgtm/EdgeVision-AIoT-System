# Deployment Target

Raspberry Pi 5
Debian Bookworm 64-bit

# Runtime Environment

Python 3.11.2
Docker 20.10
tflite-runtime 2.14
OpenCV 4.8

#Deployment Procedure

git clone ...

docker-compose build

docker-compose up

# Deployment Challenges

- TensorFlow ¡÷ TFLite migration
- MQTT TLS configuration conflict
- Docker build path mismatch
- Docker volume mapping mismatch

# Final Validation

Environment:
- Raspberry Pi 5
- Docker Compose Deployment

Workload:
- 322 image burst test

# Result:
- 322 images processed
- 322 MQTT messages published
- 322 CSV records generated
- 0 dropped frame
- 0 crash
- 0 deadlock
- graceful shutdown verified