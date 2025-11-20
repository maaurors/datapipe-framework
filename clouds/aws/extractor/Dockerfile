FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

RUN pip install boto3

ENTRYPOINT ["python", "src/extractor.py"]
