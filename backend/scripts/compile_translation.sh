#!/usr/bin/env bash

# Check if pybabel is installed
if ! command -v pybabel &> /dev/null; then
  echo "pybabel could not be found. Please install it."
  exit 1
fi

pybabel compile -d app/locales
