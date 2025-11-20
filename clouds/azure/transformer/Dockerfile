FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/

# No instalar nada adicional - solo usar Python estándar
ENTRYPOINT ["python", "src/transformer.py"]
