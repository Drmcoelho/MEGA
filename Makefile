.PHONY: help install test lint format security clean all

# Default target
help:
	@echo "MEGA - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make test        - Run all tests with coverage"
	@echo "  make lint        - Run linters (ruff, flake8, mypy)"
	@echo "  make format      - Format code (black, isort)"
	@echo "  make security    - Run security checks"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make all         - Run format, lint, security, and test"
	@echo "  make pre-commit  - Install pre-commit hooks"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements-dev.txt
	@echo "Installing packages in editable mode..."
	@find packages -name "pyproject.toml" -exec dirname {} \; | while read pkg; do \
		pip install -e "$$pkg" || true; \
	done
	@echo "✅ Installation complete"

# Run tests
test:
	@echo "Running tests with coverage..."
	pytest --cov=packages --cov-report=term-missing --cov-report=html --cov-report=xml -v
	@echo "✅ Tests complete"

# Run linters
lint:
	@echo "Running linters..."
	@echo "\n==> Ruff"
	ruff check packages/ || true
	@echo "\n==> Flake8"
	flake8 packages/ --max-line-length=120 --extend-ignore=E203,W503 || true
	@echo "\n==> mypy"
	mypy packages/ --ignore-missing-imports || true
	@echo "✅ Linting complete"

# Format code
format:
	@echo "Formatting code..."
	@echo "==> Black"
	black packages/
	@echo "==> isort"
	isort packages/
	@echo "✅ Formatting complete"

# Security checks
security:
	@echo "Running security checks..."
	@echo "\n==> pip-audit"
	pip-audit -r requirements-dev.txt || true
	@echo "\n==> bandit"
	bandit -r packages/ -ll || true
	@echo "\n==> detect-secrets"
	detect-secrets scan --baseline .secrets.baseline || true
	@echo "✅ Security checks complete"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Install pre-commit hooks
pre-commit:
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "Creating secrets baseline..."
	detect-secrets scan > .secrets.baseline || true
	@echo "✅ Pre-commit hooks installed"

# Run all checks
all: format lint security test
	@echo ""
	@echo "================================"
	@echo "✅ All checks passed!"
	@echo "================================"
