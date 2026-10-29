#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for create_variables_file.py
"""
import pytest

from cmewpy.configure_standardise.create_variables_file import (
    determine_unique_variables,
    add_stream_to_variables,
)


@pytest.mark.parametrize(
    "variable_list_1,variable_list_2,expected",
    [
        pytest.param(
            ["Amon/hfls", "Emon/rls"],
            ["Amon/tas", "SImon/siconc"],
            ["Amon/hfls", "Emon/rls", "Amon/tas", "SImon/siconc"],
            id="no overlap",
        ),
        pytest.param(
            ["Amon/hfls", "Emon/rls"],
            ["Amon/hfls", "SImon/siconc"],
            ["Amon/hfls", "Emon/rls", "SImon/siconc"],
            id="with overlap",
        ),
    ],
)
def test_determine_unique_variables(
    variable_list_1, variable_list_2, expected
):
    variable_lists = [variable_list_1, variable_list_2]
    actual = determine_unique_variables(variable_lists)
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
    expected = [
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

    actual = add_stream_to_variables(input, mock_stream_dict)
    assert actual == expected
