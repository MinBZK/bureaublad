#!/usr/bin/env bash

# Usage: ./scripts/lint.sh

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv could not be found. Please install it. For more information visit https://docs.astral.sh/uv/getting-started/installation/"
  exit 1
fi

# Check if dependencies are installed
if ! uv run --quiet python -c "import pyright" 2>/dev/null; then
  echo "Dependencies not installed. Installing..."
  uv sync
fi

uv run pyright
