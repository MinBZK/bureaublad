FROM --platform=$BUILDPLATFORM python:3.12-slim AS build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app

WORKDIR /src

# Install dependencies first (cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

# Copy application code
COPY . /src

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --locked \
        --no-dev \
        --no-editable

# Runtime stage
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/MinBZK/bureaublad"
LABEL org.opencontainers.image.description="MijnBureau Backend API"
LABEL org.opencontainers.image.licenses="EUPL-1.2"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/app/bin:$PATH

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment from build stage with root ownership and read-only permissions
COPY --from=build --chown=root:root --chmod=755 /app /app

# Switch to non-root user
USER appuser

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "bureaublad_api.main:app", "--port", "8080"]
