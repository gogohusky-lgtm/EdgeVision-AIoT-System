# Python Package Resolution in Dockerized AIoT System

## Background

During the transition from a single-node AI inference script into a modularized multi-service AIoT architecture, multiple `ModuleNotFoundError` issues appeared inside Docker containers.

Typical errors included:

```python
ModuleNotFoundError: No module named 'monitoring'
ModuleNotFoundError: No module named 'action_layer'
```

The issue did not occur in local execution under Windows, but consistently appeared after containerization.

---

# Root Cause

The problem was caused by a mismatch between:

* Python package resolution rules
* Docker build context
* runtime working directory
* repository structure

In the original single-node version, all Python files existed within a relatively flat directory layout, so Python imports worked implicitly.

However, after modularization:

```text
EdgeVision-AIoT-System/
¢u¢w¢w ai_engine/
¢u¢w¢w monitoring/
¢u¢w¢w action_layer/
¢u¢w¢w communication/
```

the application became a true multi-package Python project.

Inside Docker, Python only resolves imports from:

* current working directory
* installed packages
* PYTHONPATH

If the container copies only partial directories, or launches from a different path, imports fail.

---

# Initial Incorrect Design

The early Dockerfile used:

```dockerfile
COPY . /app
```

inside:

```text
ai_engine/
```

This copied only the contents of `ai_engine/` into the container.

As a result:

```python
from monitoring.logger import ...
```

failed because `/app/monitoring/` did not exist inside the container.

---

# Correct Solution

The solution was:

## 1. Build from project root

docker-compose.yml:

```yaml
build:
  context: .
  dockerfile: ai_engine/Dockerfile
```

This allows Docker to access the entire repository.

---

## 2. Copy full repository into container

Dockerfile:

```dockerfile
COPY . /app
```

Now all modules become available:

```text
/app/monitoring
/app/action_layer
/app/communication
```

---

## 3. Execute from project-root context

The runtime entry became:

```dockerfile
CMD ["python", "ai_engine/frame_to_inference.py"]
```

instead of:

```dockerfile
CMD ["python", "frame_to_inference.py"]
```

This preserved correct module resolution relative to `/app`.

---

## 4. Add **init**.py

Every importable module directory required:

```text
__init__.py
```

including:

```text
monitoring/
communication/
action_layer/
ai_engine/
```

Without these files, Python would not recognize directories as packages.

---

# Important Engineering Lesson

This issue demonstrates a key distinction:

## Script-oriented programming

vs

## Package-oriented system engineering

Small local scripts often work accidentally because execution paths are simple.

Distributed systems require:

* deterministic package structure
* explicit runtime boundaries
* stable import resolution
* reproducible deployment behavior

This transition is one of the major conceptual shifts from:

* hobby scripting

to

* production-grade AIoT engineering.

---

# Final Stable Design

Final container strategy:

```text
Repository Root
    ¡õ
Docker Build Context
    ¡õ
Copy Entire Repository
    ¡õ
Launch Service from Root
    ¡õ
Python Package Imports Resolve Correctly
```

This became the foundation for future:

* multi-container deployment
* remote nodes
* orchestration
* scalable AI inference systems
* CI/CD pipelines
* distributed runtime debugging
