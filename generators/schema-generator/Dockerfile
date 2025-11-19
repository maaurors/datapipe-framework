FROM python:3.11-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Copiar configuración de Poetry
COPY pyproject.toml ./

# Instalar dependencias sin instalar el proyecto actual
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY schema_generator.py .

RUN useradd -m -u 1000 datapipe && chown -R datapipe:datapipe /app
USER datapipe

CMD ["python", "schema_generator.py"]
