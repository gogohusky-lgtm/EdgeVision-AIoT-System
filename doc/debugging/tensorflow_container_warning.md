# TensorFlow Container Warnings

## Symptom

Container logs displayed warnings such as:

Could not load dynamic library 'libcudart.so'

Could not load dynamic library 'libnvinfer.so'

TF-TRT Warning

Unable to register cuBLAS factory

---

## Initial Concern

At first glance, these messages appear to indicate TensorFlow installation failure.

However, inference execution continued successfully.

---

## Root Cause

The container was built using:

python:3.8-slim

which provides a CPU-only environment.

TensorFlow automatically attempts to detect:

* CUDA
* cuDNN
* TensorRT

during startup.

When GPU-related libraries are absent, TensorFlow emits warning messages.

---

## Verification

The following functionality continued to work:

* model loading
* TFLite inference
* MQTT publishing
* logging

No runtime failures were observed.

---

## Resolution

No action required.

The warnings can be safely ignored for CPU-only deployments.

If GPU acceleration is required in the future, a GPU-enabled base image must be used.

---

## Lessons Learned

Not all warnings indicate failures.

Engineers should distinguish between:

* startup warnings
* recoverable runtime warnings
* critical execution failures

before attempting remediation.
