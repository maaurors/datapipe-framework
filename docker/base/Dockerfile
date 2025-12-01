# Stage 1: Builder
FROM python:3.11-slim as builder

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Export dependencies to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# Create non-root user
RUN useradd -m datapipe
USER datapipe
