#!/usr/bin/env bash
set -e

# Assuming a virtual environment exists at ./venv
VENV_PYTHON=./venv/bin/python

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python virtual environment not found at ./venv"
    echo "Please run 'python -m venv venv' and 'source venv/bin/activate' and 'pip install -r requirements-dev.txt'"
    exit 1
fi

echo "[RUFF FORMAT]"
$VENV_PYTHON -m ruff format --check .

echo "[RUFF LINT]"
$VENV_PYTHON -m ruff check .

echo "[PYTEST]"
$VENV_PYTHON -m pytest