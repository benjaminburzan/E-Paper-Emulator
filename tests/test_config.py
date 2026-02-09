"""Tests for EPD configuration files."""

import json
import os
import glob
import pytest

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "epd_emulator", "config")
REQUIRED_KEYS = {"name", "width", "height", "color", "text_color"}


def get_config_files():
    return sorted(glob.glob(os.path.join(CONFIG_DIR, "*.json")))


@pytest.fixture(params=get_config_files(), ids=lambda p: os.path.basename(p))
def config_path(request):
    return request.param


@pytest.fixture
def config_data(config_path):
    with open(config_path) as f:
        return json.load(f)


def test_config_files_exist():
    configs = get_config_files()
    assert len(configs) > 0, "No config files found"


def test_config_is_valid_json(config_data):
    assert isinstance(config_data, dict)


def test_config_has_required_keys(config_data):
    missing = REQUIRED_KEYS - set(config_data.keys())
    assert not missing, f"Missing keys: {missing}"


def test_config_dimensions_are_positive(config_data):
    assert config_data["width"] > 0, f"width must be positive, got {config_data['width']}"
    assert config_data["height"] > 0, f"height must be positive, got {config_data['height']}"


def test_config_name_matches_filename(config_path, config_data):
    expected_name = os.path.splitext(os.path.basename(config_path))[0]
    assert config_data["name"] == expected_name, (
        f"Config name '{config_data['name']}' doesn't match filename '{expected_name}'"
    )
