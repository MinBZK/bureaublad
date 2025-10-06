#!/usr/bin/env bash

# Usage: ./scripts/format.sh

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv could not be found. Please install it. For more information visit https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

# Check if dependencies are installed
if ! uv run --quiet python -c "import ruff" 2>/dev/null; then
  echo "Dependencies not installed. Installing..."
  uv sync
fi

uv run ruff format