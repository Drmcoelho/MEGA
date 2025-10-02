#!/usr/bin/env bash
# Script to validate module manifests locally
# This script ensures all dependencies are installed and runs the validation

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Module Manifest Validation ==="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "Using Python: $(python3 --version)"
echo ""

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import pydantic" 2>/dev/null; then
    echo "⚠️  pydantic not found. Installing dependencies..."
    pip install pydantic pyyaml
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    echo "⚠️  pyyaml not found. Installing dependencies..."
    pip install pyyaml
fi

echo ""

# Run validation
cd "$REPO_ROOT"
python3 scripts/validate_manifests.py
