# Quick Reference: Module Manifest Validation

## For Contributors

### Validating Locally Before Commit

```bash
# Option 1: Direct Python script
python3 scripts/validate_manifests.py

# Option 2: Convenience bash script (auto-installs dependencies)
bash scripts/validate_manifests.sh
```

### Creating a New Module Manifest

Create `content/modules/your-module-name/manifest.yaml`:

```yaml
id: your-module-name              # Required: alphanumeric, hyphens, underscores only
title: Your Module Title          # Required
version: 0.1.0                    # Required: semantic versioning (X.Y.Z)
objectives:                       # Optional
  - Learning objective 1
  - Learning objective 2
subskills:                        # Optional
  - subskill-1
  - subskill-2
prerequisites:                    # Optional
  - prerequisite-module-id
estimated_time_hours: 2           # Optional: positive number
disclaimer: Educational material  # Optional
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Field required: version` | Missing required field | Add the missing field |
| `id must contain only alphanumeric...` | Invalid characters in id | Use only letters, numbers, hyphens, underscores |
| `version must follow semantic versioning` | Wrong version format | Use format X.Y.Z (e.g., 0.1.0) |
| `estimated_time_hours must be positive` | Zero or negative time | Use a positive number |

### CI/CD

- Validation runs automatically on push/PR to `main` or `develop`
- Pull requests won't pass if manifests are invalid
- Check the GitHub Actions tab for validation results

### Getting Help

- See full documentation: [docs/manifest-validation.md](docs/manifest-validation.md)
- See schema details: [content/README.md](content/README.md)
- Run tests: `pytest tests/test_manifest_validation.py -v`
