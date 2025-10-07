"""
Tests for manifest validation script.
"""
import os
import tempfile
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

# Import from scripts directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_manifests import ModuleManifest, validate_manifest, find_manifests


def test_valid_manifest():
    """Test that a valid manifest passes validation."""
    valid_data = {
        "id": "test-module",
        "title": "Test Module",
        "version": "0.1.0",
        "objectives": ["Learn something"],
        "subskills": ["skill1"],
        "prerequisites": [],
        "estimated_time_hours": 2,
        "disclaimer": "Test disclaimer"
    }
    manifest = ModuleManifest(**valid_data)
    assert manifest.id == "test-module"
    assert manifest.title == "Test Module"


def test_minimal_valid_manifest():
    """Test that a manifest with only required fields is valid."""
    minimal_data = {
        "id": "minimal-module",
        "title": "Minimal Module"
    }
    manifest = ModuleManifest(**minimal_data)
    assert manifest.id == "minimal-module"
    assert manifest.title == "Minimal Module"
    assert manifest.version == "0.1.0"  # default value


def test_missing_required_field():
    """Test that missing required fields cause validation error."""
    with pytest.raises(ValidationError):
        ModuleManifest(id="test")  # missing title
    
    with pytest.raises(ValidationError):
        ModuleManifest(title="Test")  # missing id


def test_extra_field_not_allowed():
    """Test that extra fields not in schema are rejected."""
    with pytest.raises(ValidationError):
        ModuleManifest(
            id="test",
            title="Test",
            extra_field="not allowed"
        )


def test_validate_manifest_valid_file():
    """Test validate_manifest function with a valid file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            "id": "test-module",
            "title": "Test Module",
            "version": "0.1.0"
        }, f)
        temp_path = Path(f.name)
    
    try:
        is_valid, error_msg = validate_manifest(temp_path)
        assert is_valid is True
        assert error_msg is None
    finally:
        temp_path.unlink()


def test_validate_manifest_invalid_yaml():
    """Test validate_manifest with invalid YAML."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content:")
        temp_path = Path(f.name)
    
    try:
        is_valid, error_msg = validate_manifest(temp_path)
        assert is_valid is False
        assert "YAML parse error" in error_msg
    finally:
        temp_path.unlink()


def test_validate_manifest_empty_file():
    """Test validate_manifest with empty file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("")
        temp_path = Path(f.name)
    
    try:
        is_valid, error_msg = validate_manifest(temp_path)
        assert is_valid is False
        assert "Empty manifest file" in error_msg
    finally:
        temp_path.unlink()


def test_validate_manifest_missing_required():
    """Test validate_manifest with missing required fields."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({"id": "test-only"}, f)  # missing title
        temp_path = Path(f.name)
    
    try:
        is_valid, error_msg = validate_manifest(temp_path)
        assert is_valid is False
        assert "validation error" in error_msg.lower()
    finally:
        temp_path.unlink()


def test_objectives_must_be_list():
    """Test that objectives must be a list if provided."""
    with pytest.raises(ValidationError):
        ModuleManifest(
            id="test",
            title="Test",
            objectives="not a list"
        )


def test_estimated_time_can_be_float():
    """Test that estimated_time_hours accepts float values."""
    manifest = ModuleManifest(
        id="test",
        title="Test",
        estimated_time_hours=2.5
    )
    assert manifest.estimated_time_hours == 2.5


def test_all_real_manifests_are_valid():
    """Integration test: validate all actual manifests in the project."""
    repo_root = Path(__file__).parent.parent
    modules_dir = repo_root / "content" / "modules"
    
    if not modules_dir.exists():
        pytest.skip("Modules directory not found")
    
    manifests = find_manifests(modules_dir)
    
    if not manifests:
        pytest.skip("No manifests found")
    
    errors = []
    for manifest_path in manifests:
        module_name = manifest_path.parent.name
        is_valid, error_msg = validate_manifest(manifest_path)
        if not is_valid:
            errors.append(f"{module_name}: {error_msg}")
    
    assert len(errors) == 0, f"Found {len(errors)} invalid manifest(s):\n" + "\n".join(errors)
