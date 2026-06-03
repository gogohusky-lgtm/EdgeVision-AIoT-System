# Docker Context vs COPY

## Background

During containerization, several build failures occurred even though the required files existed in the repository.

---

## Initial Assumption

The files were present locally.

Therefore Docker should be able to copy them.

This assumption proved incorrect.

---

## Understanding Docker Context

Docker can only access files inside the build context.

Example:

docker build .

The "." directory becomes the build context.

Files outside this context are invisible to Docker.

---

## Common Mistake

Dockerfile:

COPY requirements.txt .

works only if requirements.txt exists inside the build context.

Changing project structure without updating build context causes build failures.

---

## Project Impact

Several issues were traced to:

* incorrect build context
* incorrect Dockerfile location
* incorrect COPY paths

rather than missing files.

---

## Solution

Explicitly define:

build:
context: .
dockerfile: ai_engine/Dockerfile

and verify all COPY instructions are relative to the build context.

---

## Key Lesson

Docker COPY operates relative to the build context, not relative to the Dockerfile location.

Understanding this distinction is essential for reliable containerized deployments.
