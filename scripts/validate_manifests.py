#!/usr/bin/env python3
"""
Validation script for module manifests.

This script validates that all manifest.yaml files in content/modules/
conform to the defined schema using Pydantic.
"""

import sys
import yaml
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, field_validator


class ModuleManifest(BaseModel):
    """Schema for module manifest files."""
    
    # Required fields
    id: str = Field(..., description="Unique identifier for the module")
    title: str = Field(..., description="Human-readable title of the module")
    version: str = Field(..., description="Semantic version (e.g., 0.1.0)")
    
    # Optional fields
    objectives: Optional[list[str]] = Field(
        default=None,
        description="Learning objectives for the module"
    )
    subskills: Optional[list[str]] = Field(
        default=None,
        description="Subskills covered in this module"
    )
    prerequisites: Optional[list[str]] = Field(
        default=None,
        description="Module IDs that are prerequisites"
    )
    estimated_time_hours: Optional[int | float] = Field(
        default=None,
        description="Estimated time to complete in hours"
    )
    disclaimer: Optional[str] = Field(
        default=None,
        description="Disclaimer text for the module"
    )
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate that id follows naming conventions."""
        if not v:
            raise ValueError("id cannot be empty")
        if not all(c.isalnum() or c in '-_' for c in v):
            raise ValueError("id must contain only alphanumeric characters, hyphens, or underscores")
        return v
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate that version follows semantic versioning."""
        if not v:
            raise ValueError("version cannot be empty")
        parts = v.split('.')
        if len(parts) != 3:
            raise ValueError("version must follow semantic versioning (e.g., 0.1.0)")
        try:
            for part in parts:
                int(part)
        except ValueError:
            raise ValueError("version parts must be integers")
        return v
    
    @field_validator('estimated_time_hours')
    @classmethod
    def validate_estimated_time(cls, v: Optional[int | float]) -> Optional[int | float]:
        """Validate that estimated time is positive."""
        if v is not None and v <= 0:
            raise ValueError("estimated_time_hours must be positive")
        return v


def validate_manifest(manifest_path: Path) -> tuple[bool, Optional[str]]:
    """
    Validate a single manifest file.
    
    Args:
        manifest_path: Path to the manifest.yaml file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if data is None:
            return False, "Manifest file is empty"
        
        # Validate against schema
        ModuleManifest(**data)
        return True, None
        
    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {e}"
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = '.'.join(str(x) for x in error['loc'])
            msg = error['msg']
            errors.append(f"  - {field}: {msg}")
        return False, "Validation errors:\n" + '\n'.join(errors)
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main() -> int:
    """
    Main entry point for the validation script.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Find the content/modules directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    modules_dir = repo_root / 'content' / 'modules'
    
    if not modules_dir.exists():
        print(f"❌ Error: Modules directory not found at {modules_dir}")
        return 1
    
    # Find all manifest files
    manifest_files = list(modules_dir.glob('*/manifest.yaml'))
    
    if not manifest_files:
        print(f"⚠️  Warning: No manifest files found in {modules_dir}")
        return 0
    
    print(f"Found {len(manifest_files)} manifest file(s) to validate\n")
    
    # Validate each manifest
    all_valid = True
    for manifest_path in sorted(manifest_files):
        module_name = manifest_path.parent.name
        is_valid, error_message = validate_manifest(manifest_path)
        
        if is_valid:
            print(f"✅ {module_name}: Valid")
        else:
            print(f"❌ {module_name}: Invalid")
            print(f"{error_message}\n")
            all_valid = False
    
    # Print summary
    print(f"\n{'='*60}")
    if all_valid:
        print("✅ All manifests are valid!")
        return 0
    else:
        print("❌ Some manifests have validation errors")
        print("\nPlease fix the errors above and run this script again.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
