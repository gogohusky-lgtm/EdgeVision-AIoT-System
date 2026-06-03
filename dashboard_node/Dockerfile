FROM python:3.8-slim

WORKDIR /app

COPY dashboard_node/requirements.txt .

RUN pip install --default-timeout=1000 \
    --retries 10 \
    --no-cache-dir \
    -r requirements.txt

COPY . /app

CMD ["python", "dashboard_node/dashboard_subscriber.py"]