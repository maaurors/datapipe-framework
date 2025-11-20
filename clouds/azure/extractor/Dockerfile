FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install azure-storage-blob

ENTRYPOINT ["python", "src/extractor.py"]
