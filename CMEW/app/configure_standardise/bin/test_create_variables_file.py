#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for create_variables_file.py

Test data files:
/app/unittest/mock_data/radiation_budget_variables.txt
    input for test_combine_variable_lists
/app/unittest/mock_data/seaice_variables.txt
    input for test_combine_variable_lists
/app/unittest/kgo/variables.txt
    kgo for add_stream_to_variables
"""
from create_variables_file import (
    combine_variable_lists,
    add_stream_to_variables,
)
from configure_standardise_conftest import (
    mock_data_dir,
    variables_txt_fp,
)


def test_combine_variable_lists():
    mock_vars_lists_dir = str(mock_data_dir())
    actual = combine_variable_lists(mock_vars_lists_dir)

    expected = [
        "Amon/hfls",
        "Amon/hfss",
        "Amon/rlds",
        "Emon/rls",
        "Amon/rlut",
        "Amon/rlutcs",
        "Amon/rsds",
        "Amon/rsdt",
        "Emon/rss",
        "Amon/rsut",
        "Amon/rsutcs",
        "Amon/tas",
        "SImon/siconc",
    ]

    assert actual == expected


def test_add_stream_to_variables():
    input = [
        "Amon/hfls",
        "Amon/hfss",
        "Amon/rlds",
        "Emon/rls",
        "Amon/rlut",
        "Amon/rlutcs",
        "Amon/rsds",
        "Amon/rsdt",
        "Emon/rss",
        "Amon/rsut",
        "Amon/rsutcs",
        "Amon/tas",
        "SImon/siconc",
    ]
    mock_stream_dict = {
        "apm": [
            "Amon/hfls",
            "Amon/hfss",
            "Amon/rlds",
            "Amon/rlut",
            "Amon/rlutcs",
            "Amon/rsds",
            "Amon/rsdt",
            "Amon/rsut",
            "Amon/rsutcs",
            "Amon/tas",
            "Emon/rls",
            "Emon/rss",
        ],
        "inm": [
            "SImon/siconc",
        ],
    }

    actual = add_stream_to_variables(input, mock_stream_dict)

    with open(str(variables_txt_fp()), "r") as file:
        expected = file.read().splitlines()

    assert actual == expected
