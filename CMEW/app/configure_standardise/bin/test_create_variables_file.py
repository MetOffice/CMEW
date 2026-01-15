#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Tests for configure_standardise
"""
from create_variables_file import parse_variables_from_recipe
from pathlib import Path
import pytest

pytestmark = pytest.mark.unittest


def test_parse_radiation_budget_variables():
    recipe_path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "test_radiation_budget_recipe_v2.9.0.yml"
    )
    actual = parse_variables_from_recipe(recipe_path)
    expected = [
        "Emon/rss:apm",
        "Amon/rsdt:apm",
        "Amon/rsut:apm",
        "Amon/rsutcs:apm",
        "Amon/rsds:apm",
        "Emon/rls:apm",
        "Amon/rlut:apm",
        "Amon/rlutcs:apm",
        "Amon/rlds:apm",
        "Amon/hfss:apm",
        "Amon/hfls:apm",
    ]
    assert actual == expected
