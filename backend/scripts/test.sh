#!/usr/bin/env bash

set -e
set -x


if ! uv run coverage run ; then
    echo "pytest test failed"
    exit 1
fi


uv run coverage report
uv run coverage html
uv run coverage lcov
