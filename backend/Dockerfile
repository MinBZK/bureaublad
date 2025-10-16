FROM --platform=$BUILDPLATFORM python:3.13-slim AS build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/venv

WORKDIR /app

# Copy application code
COPY . /app

# Install the project
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-editable

# Runtime stage
FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/MinBZK/bureaublad"
LABEL org.opencontainers.image.description="MijnBureau Backend API"
LABEL org.opencontainers.image.licenses="EUPL-1.2"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/venv/bin:$PATH \
    PYTHONPATH=/app/

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment from build stage with root ownership and read-only permissions
COPY --from=build --chown=root:root --chmod=755 /venv /venv
COPY --from=build --chown=root:root --chmod=755 /app /app

# Switch to non-root user
USER appuser
EXPOSE 8000

# Run the application
ENTRYPOINT ["/venv/bin/uvicorn"]
CMD ["--host", "0.0.0.0", "app.main:app", "--port", "8000"]
