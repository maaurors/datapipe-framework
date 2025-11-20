FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY src/ ./src/

ENTRYPOINT ["python", "src/table_generator.py"]
