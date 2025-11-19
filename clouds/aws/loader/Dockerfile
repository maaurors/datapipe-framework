FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install redshift-connector boto3 structlog

CMD ["python", "src/loader.py"]
