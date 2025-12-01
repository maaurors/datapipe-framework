FROM datapipe/base:latest

USER datapipe
WORKDIR /app

COPY src/ ./src/

ENTRYPOINT ["python", "src/loader.py"]
