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
from pathlib import Path
import pytest
import tempfile


@pytest.fixture
def mock_env_vars(monkeypatch):
    # For adding to variables
    monkeypatch.setenv("STREAM_ID", "apm")


@pytest.fixture
def path_to_combined_variables():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "variables.txt"
    )
    return str(path)


def test_combine_variable_lists():
    actual = combine_variable_lists(
        str(Path(__file__).parent.parent.parent / "unittest" / "mock_data")
    )

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
        "fx/areacello",
        "OImon/sic",
    ]

    assert actual == expected


def test_add_stream_to_variables(mock_env_vars, path_to_combined_variables):
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
        "fx/areacello",
        "OImon/sic",
    ]
    actual = add_stream_to_variables(input)

    with open(path_to_combined_variables, "r") as file:
        expected = file.read().splitlines()

    assert actual == expected


def test_write_variables(path_to_combined_variables):
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
        "fx/areacello:apm",
        "OImon/sic:apm",
    ]

    # Write the test dictionary to a temporary file
    with tempfile.NamedTemporaryFile() as tmp:
        write_variables(input, tmp.name)
        tmp.seek(0)
        actual = tmp.read().decode("utf-8")  # decode bytes to string

    # Load the expected list
    with open(path_to_combined_variables, "r") as file_handle:
        expected = file_handle.read()

    assert expected == actual
