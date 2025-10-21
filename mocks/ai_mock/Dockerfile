FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock .
RUN uv sync --frozen --no-dev

COPY main.py .

EXPOSE 1080

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1080"]
