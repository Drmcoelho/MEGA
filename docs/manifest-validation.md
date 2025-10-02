# Module Manifest Validation

This document describes the manifest validation system for module manifests in the MEGA project.

## Overview

Module manifests (`content/modules/*/manifest.yaml`) follow a strict schema defined using Pydantic. This ensures consistency and correctness across all educational modules.

## Schema

### Required Fields

- **id** (string): Unique identifier for the module
  - Must contain only alphanumeric characters, hyphens, or underscores
  - Example: `ecg-basics`, `arrhythmias-basics`

- **title** (string): Human-readable title of the module
  - Example: `ECG Básico`, `Arritmias Básicas`

- **version** (string): Semantic version of the module
  - Format: `MAJOR.MINOR.PATCH` (e.g., `0.1.0`, `1.2.3`)
  - All parts must be integers

### Optional Fields

- **objectives** (list of strings): Learning objectives
- **subskills** (list of strings): Subskills covered in the module
- **prerequisites** (list of strings): Module IDs that are prerequisites
- **estimated_time_hours** (number): Estimated time to complete (must be positive)
- **disclaimer** (string): Disclaimer text for the module

## Validation

### Local Validation

To validate manifests locally:

```bash
# Quick validation
python3 scripts/validate_manifests.py

# Or use the convenience script
bash scripts/validate_manifests.sh
```

### CI/CD

Manifests are automatically validated in CI/CD via GitHub Actions:
- On every push to `main` or `develop` branches
- On every pull request

The workflow runs:
1. Schema validation of all manifests
2. Unit tests for the validation logic

### Error Messages

The validation script provides clear, actionable error messages:

```
❌ module-name: Invalid
Validation errors:
  - version: Field required
  - id: Value error, id must contain only alphanumeric characters, hyphens, or underscores
```

## Testing

The validation system includes comprehensive tests:

```bash
pytest tests/test_manifest_validation.py -v
```

Tests cover:
- Valid minimal and complete manifests
- Missing required fields
- Invalid field formats
- Edge cases (empty values, special characters, etc.)
- Validation of existing manifests in the repository

## Dependencies

- Python 3.11+
- pydantic >= 2.0
- pyyaml
- pytest (for testing)

Install dependencies:
```bash
pip install -r requirements-dev.txt
```

## Contributing

When adding or modifying module manifests:

1. Ensure your manifest follows the schema documented in `content/README.md`
2. Run local validation: `python3 scripts/validate_manifests.py`
3. Fix any validation errors reported
4. Submit your pull request - CI will validate automatically

## Implementation Details

- **Validation Script**: `scripts/validate_manifests.py`
- **Tests**: `tests/test_manifest_validation.py`
- **CI Workflow**: `.github/workflows/validate-manifests.yml`
- **Schema Documentation**: `content/README.md`
