# MEGA

## Development

### Module Manifest Validation

Module manifests in `content/modules/*/manifest.yaml` follow a strict schema. To validate manifests:

**Local validation:**
```bash
# Quick validation
python3 scripts/validate_manifests.py

# Or use the convenience script
bash scripts/validate_manifests.sh
```

**CI validation:**
Manifests are automatically validated on every push/PR via GitHub Actions.

For schema documentation, see [content/README.md](content/README.md).