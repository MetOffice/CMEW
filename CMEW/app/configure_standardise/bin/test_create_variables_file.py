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
    write_variables,
)
import tempfile
from configure_standardise_conftest import (
    mock_data_dir,
    variables_txt_fp,
    streams_yml_fp,
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
    actual = add_stream_to_variables(str(streams_yml_fp()), input)

    with open(str(variables_txt_fp()), "r") as file:
        expected = file.read().splitlines()

    assert actual == expected


def test_write_variables():
    input = [
        "Amon/hfls:apm",
        "Amon/hfss:apm",
        "Amon/rlds:apm",
        "Emon/rls:apm",
        "Amon/rlut:apm",
        "Amon/rlutcs:apm",
        "Amon/rsds:apm",
        "Amon/rsdt:apm",
        "Emon/rss:apm",
        "Amon/rsut:apm",
        "Amon/rsutcs:apm",
        "Amon/tas:apm",
        "SImon/siconc:inm",
    ]

    # Write the test dictionary to a temporary file
    with tempfile.NamedTemporaryFile() as tmp:
        write_variables(input, tmp.name)
        tmp.seek(0)
        actual = tmp.read().decode("utf-8")  # decode bytes to string

    # Load the expected list
    with open(str(variables_txt_fp()), "r") as file_handle:
        expected = file_handle.read()

    assert expected == actual
