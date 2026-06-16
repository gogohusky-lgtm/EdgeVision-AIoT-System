FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY deployment/ai_node/requirements.txt .

RUN pip install --default-timeout=1000 \
    --retries 10 \
    --no-cache-dir \
    -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src

CMD ["python", "-u", "src/runtime/frame_to_inference.py"]
