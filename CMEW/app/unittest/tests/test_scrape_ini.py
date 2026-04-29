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
def path_to_correct_ini():
    path = Path(__file__).parent.parent / "mock_data" / "ini_files" / "correct.ini"
    return str(path)


@pytest.fixture
def path_to_duplicate_headers():
    path = Path(__file__).parent.parent / "mock_data" / "ini_files" / "duplicate_header.ini"
    return str(path)


@pytest.fixture
def path_to_duplicate_suite_id():
    path = Path(__file__).parent.parent / "mock_data" / "ini_files" / "duplicate_suite_id.ini"
    return str(path)


@pytest.fixture
def path_to_missing_suite_id():
    path = Path(__file__).parent.parent / "mock_data" / "ini_files" / "missing_suite_id.ini"
    return str(path)


def test_list_datasets_correct(path_to_correct_ini):
    expected = "line_12, line_15, line_19"
    actual = scrape_ini.list_datasets(path_to_correct_ini)
    assert actual == expected


def test_list_datasets_duplicate_section(path_to_duplicate_headers):
    with pytest.raises(ValueError):
        scrape_ini.list_datasets(path_to_duplicate_headers)


def test_list_datasets_duplicate_suite(path_to_duplicate_suite_id):
    with pytest.raises(ValueError):
        scrape_ini.list_datasets(path_to_duplicate_suite_id)


def test_list_datasets_missing_suite(path_to_missing_suite_id):
    with pytest.raises(ValueError):
        scrape_ini.list_datasets(path_to_missing_suite_id)
