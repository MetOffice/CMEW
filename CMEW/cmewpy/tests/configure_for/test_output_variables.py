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
from cmewpy.configure_for.output_variables import (
    parse_variables_from_recipe,
    write_variables,
)
import tempfile


def test_parse_variables_from_outer_key(
    path_to_original_radiation_budget_recipe,
):
    actual = parse_variables_from_recipe(
        path_to_original_radiation_budget_recipe
    )
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

    # Load the expected list
    with open(path_to_radiation_budget_variables, "r") as file_handle:
        expected = file_handle.read()

    assert expected == actual
