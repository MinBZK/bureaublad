FROM --platform=$BUILDPLATFORM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY app/ /app/app
COPY uv.lock pyproject.toml /app/

# Install the application dependencies.
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/venv
RUN uv sync --frozen --no-cache

ENV PYTHONPATH=/app/

# Run the application.
ENTRYPOINT [ "/venv/bin/uvicorn" ]
CMD ["--host", "0.0.0.0", "app.main:app", "--port", "8000"]