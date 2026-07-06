# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Unit tests for CMEW/lib/python/scrape_ini.py"""
from cmewpy.common import scrape_ini


def test_list_datasets_correct(path_to_mock_ini):
    expected = "line_9, line_12, line_16"
    actual = scrape_ini.list_datasets(path_to_mock_ini)
    assert actual == expected


def test_ref_dataset_extracted(path_to_mock_ini):
    expected = "line_16"
    actual = scrape_ini.find_ref(path_to_mock_ini)
    assert actual == expected
