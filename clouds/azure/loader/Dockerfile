FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install azure-identity azure-synapse-artifacts structlog

CMD ["python", "src/loader.py"]
