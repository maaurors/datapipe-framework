FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN useradd -m -u 1000 datapipe && chown -R datapipe:datapipe /app
USER datapipe

CMD ["echo", "Table Generator - En desarrollo"]
