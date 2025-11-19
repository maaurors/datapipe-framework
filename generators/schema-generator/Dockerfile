FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY schema_generator.py .

RUN useradd -m -u 1000 datapipe && chown -R datapipe:datapipe /app
USER datapipe

CMD ["python", "schema_generator.py"]
