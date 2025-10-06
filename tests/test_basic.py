"""
Basic test to verify CI functionality
"""
import pytest


def test_basic_functionality():
    """Test that basic Python functionality works"""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations"""
    text = "MEGA"
    assert text.lower() == "mega"
    assert len(text) == 4


def test_list_operations():
    """Test list operations"""
    items = [1, 2, 3]
    items.append(4)
    assert len(items) == 4
    assert 4 in items


def test_dict_operations():
    """Test dictionary operations"""
    config = {"name": "MEGA", "version": "0.1.0"}
    assert config["name"] == "MEGA"
    assert config.get("version") == "0.1.0"
    assert config.get("missing", "default") == "default"


if __name__ == "__main__":
    pytest.main([__file__])