FROM python:3.11-slim

WORKDIR /app

COPY deployment/dashboard_node/requirements.txt .

RUN pip install --default-timeout=1000 \
    --retries 10 \
    --no-cache-dir \
    -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src

CMD ["python", "src/dashboard/dashboard_subscriber.py"]
