#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for output_variables.py

Test data files:
/app/unittest/mock_data/original_recipe_radiation_budget.yml
    input for test_parse_variables_from_recipe
/app/unittest/kgo/radiation_budget_variables.txt
    kgo for test_write_variables
"""
from output_variables import parse_variables_from_recipe, write_variables
from pathlib import Path
import pytest
import tempfile


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
def path_to_radiation_budget_variables():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "radiation_budget_variables.txt"
    )
    return path



def test_parse_variables_from_recipe(path_to_radiation_budget_recipe):

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


def test_write_variables(path_to_radiation_budget_variables):
    input = [
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

    # Write the test dictionary to a temporary file
    with tempfile.NamedTemporaryFile() as tmp:
        write_variables(input, tmp.name)
        tmp.seek(0)
        actual = tmp.read().decode("utf-8")  # decode bytes to string

    # Load the expected dictionary
    with open(path_to_radiation_budget_variables, "r") as file_handle:
        expected = file_handle.read()

    assert expected == actual
