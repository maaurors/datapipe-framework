FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install structlog

ENTRYPOINT ["python", "src/transformer.py"]
