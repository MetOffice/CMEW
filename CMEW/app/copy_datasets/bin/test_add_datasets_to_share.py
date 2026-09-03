# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.nl
    input for test_extract_sections_from_naml
    input for test_process_naml_file
"""
from add_datasets_to_share import (
    extract_sections_from_naml,
    convert_str_to_facets,
    add_common_facets,
    process_naml_file,
    list_files,
    use_facet_as_key,
)
import pytest
from unittest.mock import patch
from copy_datasets_conftest import model_runs_nl_fp

START_YEAR = "1993"
NUMBER_OF_YEARS = "10"
INSTITUTE = "mock_institute"


def test_extract_sections_from_naml():
    # Note that I actually expect one long string for each section,
    # not a concatenated string, but this fails the flake8 tests.
    expected = [
        (
            "calendar=gregorian,"
            "label_for_plots=HadGEM3-GC5E-LL N96ORCA1,"
            "model_id=HadGEM3-GC5E-LL,"
            "suite_id=u-cw673,"
            "variant_label=r1i1p1f1,"
        ),
        (
            "calendar=360_day,"
            "label_for_plots=HadGEM3-GC3.1 N96ORCA1,"
            "model_id=HadGEM3-GC31-LL,"
            "suite_id=u-bv526,"
            "variant_label=r5i1p1f3,"
        ),
    ]

    actual = extract_sections_from_naml(str(model_runs_nl_fp()))
    assert actual == expected


def test_convert_str_to_facets():
    section = (
        "calendar=gregorian,"
        "label_for_plots=HadGEM3-GC5E-LL N96ORCA1,"
        "model_id=HadGEM3-GC5E-LL,"
        "suite_id=u-cw673,"
        "variant_label=r1i1p1f1,"
    )
    expected = {
        "calendar": "gregorian",
        "label_for_plots": "HadGEM3-GC5E-LL N96ORCA1",
        "model_id": "HadGEM3-GC5E-LL",
        "suite_id": "u-cw673",
        "variant_label": "r1i1p1f1",
    }

    actual = convert_str_to_facets(section)
    assert actual == expected


def test_add_common_facets():
    dataset_dict = {
        "calendar": "gregorian",
        "label_for_plots": "HadGEM3-GC5E-LL N96ORCA1",
        "model_id": "HadGEM3-GC5E-LL",
        "suite_id": "u-cw673",
        "variant_label": "r1i1p1f1",
    }

    expected = {
        "calendar": "gregorian",
        "label_for_plots": "HadGEM3-GC5E-LL N96ORCA1",
        "model_id": "HadGEM3-GC5E-LL",
        "suite_id": "u-cw673",
        "variant_label": "r1i1p1f1",
        "start_year": 1993,
        "end_year": 2002,
        "project": "CMIP6",
    }

    actual = add_common_facets(
        START_YEAR, NUMBER_OF_YEARS, dataset_dict, INSTITUTE, "CMIP6"
    )
    assert actual == expected


def test_process_naml_file():
    expected = [
        {
            "calendar": "gregorian",
            "label_for_plots": "HadGEM3-GC5E-LL N96ORCA1",
            "model_id": "HadGEM3-GC5E-LL",
            "suite_id": "u-cw673",
            "variant_label": "r1i1p1f1",
            "start_year": 1993,
            "end_year": 2002,
            "project": "CMIP6",
        },
        {
            "calendar": "360_day",
            "label_for_plots": "HadGEM3-GC3.1 N96ORCA1",
            "model_id": "HadGEM3-GC31-LL",
            "suite_id": "u-bv526",
            "variant_label": "r5i1p1f3",
            "start_year": 1993,
            "end_year": 2002,
            "project": "CMIP6",
        },
    ]

    actual = process_naml_file(
        str(model_runs_nl_fp()),
        START_YEAR,
        NUMBER_OF_YEARS,
        INSTITUTE,
        "CMIP6",
    )
    assert actual == expected


@pytest.mark.parametrize("extension", ["nl", ".nl"])
@patch("os.path.dirname", return_value="/a/b/c")
@patch(
    "os.listdir",
    return_value=[
        "this_one.nl",
        "this_two.nl",
        "not_this_one.txt",
        "subdir",
    ],
)
def test_list_files(mock_listdir, mock_dirname, extension):
    expected = {
        "this_one": "/a/b/c/this_one.nl",
        "this_two": "/a/b/c/this_two.nl",
    }
    mock_src_dir = "/a/b/c"
    actual = list_files(mock_src_dir, extension)
    assert expected == actual


def test_use_facet_as_key():
    input = [
        {
            "key_1": "value_1.1",
            "key_2": 2,
            "key_3": {"inner_key": "inner_value_1"},
            "chosen_key": "first_entry",
        },
        {
            "key_1": "value_1.2",
            "key_2": 4,
            "key_3": {"inner_key": "inner_value_2"},
            "chosen_key": "second_entry",
        },
    ]
    expected = {
        "first_entry": {
            "key_1": "value_1.1",
            "key_2": 2,
            "key_3": {"inner_key": "inner_value_1"},
            "chosen_key": "first_entry",
        },
        "second_entry": {
            "key_1": "value_1.2",
            "key_2": 4,
            "key_3": {"inner_key": "inner_value_2"},
            "chosen_key": "second_entry",
        },
    }
    actual = use_facet_as_key(input, "chosen_key")
    assert actual == expected
