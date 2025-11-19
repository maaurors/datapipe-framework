FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install google-cloud-bigquery structlog

CMD ["python", "src/loader.py"]
