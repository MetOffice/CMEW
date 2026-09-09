#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for output_variables.py

Test data files:
/app/unittest/mock_data/original_recipe_radiation_budget.yml
    input for test_parse_variables_from_outer_key
/app/unittest/mock_data/original_recipe_zec.yml
    input for test_parse_variables_from_short_name_key
/app/unittest/kgo/radiation_budget_variables.txt
    kgo for test_write_variables
"""
from get_variables_from_recipe import parse_variables_from_recipe
from pathlib import Path
import pytest


@pytest.fixture
def path_to_radiation_budget_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "original_recipe_radiation_budget.yml"
    )
    return str(path)


@pytest.fixture
def path_to_zec_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "original_recipe_zec.yml"
    )
    return str(path)


@pytest.fixture
def path_to_radiation_budget_variables():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "radiation_budget_variables.txt"
    )
    return path


def test_parse_variables_from_outer_key(path_to_radiation_budget_recipe):
    actual = parse_variables_from_recipe(path_to_radiation_budget_recipe)
    expected = [
        "Emon/rss",
        "Amon/rsdt",
        "Amon/rsut",
        "Amon/rsutcs",
        "Amon/rsds",
        "Emon/rls",
        "Amon/rlut",
        "Amon/rlutcs",
        "Amon/rlds",
        "Amon/hfss",
        "Amon/hfls",
    ]
    assert actual == expected


def test_parse_variables_from_short_name_key(path_to_zec_recipe):
    actual = parse_variables_from_recipe(path_to_zec_recipe)
    expected = ["Amon/tas"]
    assert actual == expected
