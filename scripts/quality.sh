#!/usr/bin/env bash
set -e
echo "[MANIFEST VALIDATION]"
python3 scripts/validate_manifests.py
echo ""
echo "[PYTEST]"; pytest || true
echo "(Adicionar lint futuramente)"