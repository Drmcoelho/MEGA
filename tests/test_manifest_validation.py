"""
Tests for the manifest validation script.
"""

import pytest
import yaml
from pathlib import Path
from pydantic import ValidationError
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate_manifests import ModuleManifest, validate_manifest


class TestModuleManifestSchema:
    """Test the ModuleManifest Pydantic model."""
    
    def test_valid_minimal_manifest(self):
        """Test that a minimal valid manifest passes validation."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0'
        }
        manifest = ModuleManifest(**data)
        assert manifest.id == 'test-module'
        assert manifest.title == 'Test Module'
        assert manifest.version == '1.0.0'
    
    def test_valid_complete_manifest(self):
        """Test that a complete valid manifest passes validation."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0',
            'objectives': ['Learn X', 'Learn Y'],
            'subskills': ['skill-1', 'skill-2'],
            'prerequisites': ['prereq-module'],
            'estimated_time_hours': 2.5,
            'disclaimer': 'Educational material only'
        }
        manifest = ModuleManifest(**data)
        assert manifest.objectives == ['Learn X', 'Learn Y']
        assert manifest.estimated_time_hours == 2.5
    
    def test_missing_required_id(self):
        """Test that missing id field raises validation error."""
        data = {
            'title': 'Test Module',
            'version': '1.0.0'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'id' in str(exc_info.value)
    
    def test_missing_required_title(self):
        """Test that missing title field raises validation error."""
        data = {
            'id': 'test-module',
            'version': '1.0.0'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'title' in str(exc_info.value)
    
    def test_missing_required_version(self):
        """Test that missing version field raises validation error."""
        data = {
            'id': 'test-module',
            'title': 'Test Module'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'version' in str(exc_info.value)
    
    def test_invalid_id_characters(self):
        """Test that invalid characters in id raise validation error."""
        data = {
            'id': 'test module!',  # spaces and special chars not allowed
            'title': 'Test Module',
            'version': '1.0.0'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'alphanumeric' in str(exc_info.value).lower()
    
    def test_empty_id(self):
        """Test that empty id raises validation error."""
        data = {
            'id': '',
            'title': 'Test Module',
            'version': '1.0.0'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'empty' in str(exc_info.value).lower()
    
    def test_invalid_version_format(self):
        """Test that invalid version format raises validation error."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0'  # should be X.Y.Z
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'semantic versioning' in str(exc_info.value).lower()
    
    def test_version_with_non_numeric_parts(self):
        """Test that version with non-numeric parts raises validation error."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.x'
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'integer' in str(exc_info.value).lower()
    
    def test_negative_estimated_time(self):
        """Test that negative estimated time raises validation error."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0',
            'estimated_time_hours': -1
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'positive' in str(exc_info.value).lower()
    
    def test_zero_estimated_time(self):
        """Test that zero estimated time raises validation error."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0',
            'estimated_time_hours': 0
        }
        with pytest.raises(ValidationError) as exc_info:
            ModuleManifest(**data)
        assert 'positive' in str(exc_info.value).lower()
    
    def test_valid_hyphenated_id(self):
        """Test that hyphenated id is valid."""
        data = {
            'id': 'test-module-name',
            'title': 'Test Module',
            'version': '1.0.0'
        }
        manifest = ModuleManifest(**data)
        assert manifest.id == 'test-module-name'
    
    def test_valid_underscored_id(self):
        """Test that underscored id is valid."""
        data = {
            'id': 'test_module_name',
            'title': 'Test Module',
            'version': '1.0.0'
        }
        manifest = ModuleManifest(**data)
        assert manifest.id == 'test_module_name'
    
    def test_empty_arrays_allowed(self):
        """Test that empty arrays are valid for optional list fields."""
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0',
            'objectives': [],
            'subskills': [],
            'prerequisites': []
        }
        manifest = ModuleManifest(**data)
        assert manifest.objectives == []
        assert manifest.subskills == []
        assert manifest.prerequisites == []


class TestValidateManifestFunction:
    """Test the validate_manifest function."""
    
    def test_validate_valid_manifest_file(self, tmp_path):
        """Test validating a valid manifest file."""
        manifest_file = tmp_path / "manifest.yaml"
        data = {
            'id': 'test-module',
            'title': 'Test Module',
            'version': '1.0.0'
        }
        with open(manifest_file, 'w') as f:
            yaml.dump(data, f)
        
        is_valid, error = validate_manifest(manifest_file)
        assert is_valid is True
        assert error is None
    
    def test_validate_invalid_manifest_missing_field(self, tmp_path):
        """Test validating an invalid manifest with missing required field."""
        manifest_file = tmp_path / "manifest.yaml"
        data = {
            'id': 'test-module',
            'title': 'Test Module'
            # missing version
        }
        with open(manifest_file, 'w') as f:
            yaml.dump(data, f)
        
        is_valid, error = validate_manifest(manifest_file)
        assert is_valid is False
        assert error is not None
        assert 'version' in error.lower()
    
    def test_validate_empty_manifest(self, tmp_path):
        """Test validating an empty manifest file."""
        manifest_file = tmp_path / "manifest.yaml"
        manifest_file.write_text('')
        
        is_valid, error = validate_manifest(manifest_file)
        assert is_valid is False
        assert 'empty' in error.lower()
    
    def test_validate_invalid_yaml(self, tmp_path):
        """Test validating a file with invalid YAML syntax."""
        manifest_file = tmp_path / "manifest.yaml"
        manifest_file.write_text('id: test\n  invalid: yaml: syntax')
        
        is_valid, error = validate_manifest(manifest_file)
        assert is_valid is False
        assert 'yaml' in error.lower()
    
    def test_validate_manifest_with_validation_errors(self, tmp_path):
        """Test validating a manifest with schema validation errors."""
        manifest_file = tmp_path / "manifest.yaml"
        data = {
            'id': 'test module',  # invalid: contains space
            'title': 'Test Module',
            'version': '1.0.0'
        }
        with open(manifest_file, 'w') as f:
            yaml.dump(data, f)
        
        is_valid, error = validate_manifest(manifest_file)
        assert is_valid is False
        assert error is not None
        assert 'validation' in error.lower()


class TestExistingManifests:
    """Test that existing manifests in the repository are valid."""
    
    def test_all_existing_manifests_valid(self):
        """Test that all existing manifests in content/modules are valid."""
        # Find the repo root
        test_dir = Path(__file__).parent
        repo_root = test_dir.parent
        modules_dir = repo_root / 'content' / 'modules'
        
        if not modules_dir.exists():
            pytest.skip("Modules directory not found")
        
        manifest_files = list(modules_dir.glob('*/manifest.yaml'))
        
        if not manifest_files:
            pytest.skip("No manifest files found")
        
        # Validate each manifest
        for manifest_path in manifest_files:
            is_valid, error = validate_manifest(manifest_path)
            assert is_valid, f"Manifest {manifest_path.parent.name} is invalid: {error}"
