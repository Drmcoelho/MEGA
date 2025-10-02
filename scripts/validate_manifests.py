#!/usr/bin/env python3
"""
Validate module manifest schema for MEGA project.

This script validates all manifest.yaml files in content/modules/
against the defined Pydantic schema.
"""
import os
import sys
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ModuleManifest(BaseModel):
    """Schema for module manifest files.
    
    Based on the TypeScript interface in apps/web/lib/loadModules.ts
    """
    model_config = ConfigDict(extra="forbid")  # Don't allow extra fields not in schema
    
    id: str = Field(..., description="Unique module identifier (kebab-case)")
    title: str = Field(..., description="Human-readable module title")
    version: Optional[str] = Field(default="0.1.0", description="Semantic version")
    objectives: Optional[List[str]] = Field(default=None, description="Learning objectives")
    subskills: Optional[List[str]] = Field(default=None, description="Subskills covered")
    prerequisites: Optional[List[str]] = Field(default=None, description="Required prior modules")
    estimated_time_hours: Optional[float] = Field(default=None, description="Estimated completion time in hours")
    disclaimer: Optional[str] = Field(default=None, description="Legal/educational disclaimer")


def find_manifests(base_dir: Path) -> List[Path]:
    """Find all manifest.yaml files in the modules directory."""
    manifests = []
    if not base_dir.exists():
        return manifests
    
    for module_dir in base_dir.iterdir():
        if module_dir.is_dir():
            manifest_path = module_dir / "manifest.yaml"
            if manifest_path.exists():
                manifests.append(manifest_path)
    
    return sorted(manifests)


def validate_manifest(manifest_path: Path) -> tuple[bool, Optional[str]]:
    """Validate a single manifest file.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if data is None:
            return False, "Empty manifest file"
        
        # Validate against schema
        ModuleManifest(**data)
        return True, None
        
    except yaml.YAMLError as e:
        return False, f"YAML parse error: {e}"
    except ValidationError as e:
        return False, f"Schema validation error:\n{e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    """Main validation function."""
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    modules_dir = repo_root / "content" / "modules"
    
    print(f"Validating manifests in: {modules_dir}")
    print("-" * 60)
    
    manifests = find_manifests(modules_dir)
    
    if not manifests:
        print("No manifests found.")
        return 0
    
    print(f"Found {len(manifests)} manifest(s) to validate.\n")
    
    all_valid = True
    errors = []
    
    for manifest_path in manifests:
        module_name = manifest_path.parent.name
        is_valid, error_msg = validate_manifest(manifest_path)
        
        if is_valid:
            print(f"✓ {module_name}: VALID")
        else:
            print(f"✗ {module_name}: INVALID")
            print(f"  File: {manifest_path}")
            print(f"  Error: {error_msg}")
            print()
            all_valid = False
            errors.append((module_name, error_msg))
    
    print("-" * 60)
    if all_valid:
        print(f"✓ All {len(manifests)} manifest(s) are valid!")
        return 0
    else:
        print(f"✗ {len(errors)} manifest(s) failed validation.")
        print("\nSummary of errors:")
        for module_name, error_msg in errors:
            print(f"  - {module_name}: {error_msg.split(':')[0]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
