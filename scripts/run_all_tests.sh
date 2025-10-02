#!/usr/bin/env bash
set -e
echo "== Frontend tests =="
pnpm test
echo "== Python tests =="
pytest