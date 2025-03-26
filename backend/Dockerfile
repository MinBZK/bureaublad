FROM --platform=$BUILDPLATFORM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY app/ /app
COPY uv.lock pyproject.toml /app/

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

WORKDIR /
ENV PYTHONPATH=/

# Run the application.
CMD ["/app/.venv/bin/uvicorn", "--host", "0.0.0.0", "app.main:app", "--port", "8080"]