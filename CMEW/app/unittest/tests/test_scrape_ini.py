# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Unit tests for CMEW/lib/python/scrape_ini.py"""
from pathlib import Path
import importlib.util
import pytest

# --- Section to import scrape_ini.py ---

# PYTHONPATH doesn't autmatically pick this up
scrape_ini_path = (
    Path(__file__).parent.parent.parent.parent
    / "lib"
    / "python"
    / "scrape_ini.py"
)

# The next three lines are with help from GiHub Copilot Enterprise
spec = importlib.util.spec_from_file_location("scrape_ini", scrape_ini_path)
scrape_ini = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scrape_ini)

# --- End of import section ---


@pytest.fixture
def path_to_mock_rose_suite():
    path = Path(__file__).parent.parent / "mock_data" / "config.ini"
    return str(path)

@pytest.fixture
def path_to_duplicate_header():
    path = Path(__file__).parent.parent / "mock_data" / "duplicate_header.ini"
    return str(path)

@pytest.fixture
def path_to_missing_suite_id():
    path = Path(__file__).parent.parent / "mock_data" / "missing_suite.ini"
    return str(path)


def test_list_correct_ini(path_to_mock_rose_suite):
    expected = "line_18, line_25, line_30"
    actual = scrape_ini.list_datasets(path_to_mock_rose_suite)
    assert actual == expected

def test_duplicate_header(path_to_duplicate_header):
    with pytest.raises(scrape_ini.ConfigError):
        scrape_ini.list_datasets(path_to_duplicate_header)

def test_missing_suite_id(path_to_missing_suite_id):
    with pytest.raises(scrape_ini.ConfigError):
        scrape_ini.list_datasets(path_to_missing_suite_id)
