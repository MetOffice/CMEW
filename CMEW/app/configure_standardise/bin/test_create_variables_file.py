#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
"""
Tests for configure_standardise
"""
from create_variables_file import parse_variables_from_recipe
from pathlib import Path


def test_parse_radiation_budget_variables():
    mock_path = Path(__file__).parent.parent / "mock_data" / "variables.txt"
    actual = parse_variables_from_recipe(mock_path)
    expected = """Emon/rss:apm
Amon/rsdt:apm
Amon/rsut:apm
Amon/rsutcs:apm
Amon/rsds:apm
Emon/rls:apm
Amon/rlut:apm
Amon/rlutcs:apm
Amon/rlds:apm
Amon/hfss:apm
Amon/hfls:apm
"""
    assert actual == expected
