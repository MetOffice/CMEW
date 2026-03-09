# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from add_datasets_to_share import (
    extract_sections_from_naml,
    convert_str_to_facets,
    add_common_facets,
    process_naml_file,
    write_dict_to_yaml,
    write_datasets_to_yaml,
    dict_namelists_in_work_dir,
    use_facet_as_key,
)
from pathlib import Path
import pytest
import yaml
import shutil
import tempfile
from unittest.mock import patch


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "10")
    monkeypatch.setenv("CYLC_TASK_WORK_DIR", "/a/b/c")


@pytest.fixture
def path_to_mock_nl():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "model_runs.nl"
    )
    return str(path)


@pytest.fixture
def path_to_kgo_dict():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "basic_dict.yml"
    )
    return path


@pytest.fixture
def path_to_mock_yaml_list():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "model_runs_as_list.yml"
    )
    return str(path)


@pytest.fixture
def path_to_kgo_yaml_dict():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "model_runs_as_dict.yml"
    )
    return str(path)


def test_extract_sections_from_naml(path_to_mock_nl):
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

    actual = extract_sections_from_naml(path_to_mock_nl)
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


def test_add_common_facets(mock_env_vars):
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

    actual = add_common_facets(dataset_dict)
    assert actual == expected


def test_process_naml_file(path_to_mock_nl, mock_env_vars):
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

    actual = process_naml_file(path_to_mock_nl)
    assert actual == expected


def test_write_dict_to_yaml(path_to_kgo_dict):
    # Note the keys are not alphabetical here but are in the output
    test_dict = {
        "key_1": "value_1",
        "key_for_list": ["item_1", "item_2", "item_3"],
        "key_for_dict": {
            "nested_key_1": "nested_value_1",
            "nested_key_2": "nested_value_2",
        },
    }

    # Write the test dictionary to a temporary file
    with tempfile.NamedTemporaryFile() as tmp:
        write_dict_to_yaml(test_dict, tmp.name)
        tmp.seek(0)
        actual = yaml.safe_load(tmp)

    # Load the expected dictionary
    with open(path_to_kgo_dict, "r") as file_handle:
        expected = yaml.safe_load(file_handle)

    assert expected == actual


# I tested most of the functionality above, so this just checks the filename
@patch("add_datasets_to_share.write_dict_to_yaml", return_value=None)
def test_write_datasets_to_yaml(mock_writing):

    write_datasets_to_yaml({"key": "value"}, "test_name", "/a/b")

    # Filepath should be the second ([1]) argument of the call
    assert mock_writing.call_args.args[1] == "/a/b/test_name.yml"


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
def test_dict_namelists_in_work_dir(mock_dirname, mock_listdir, mock_env_vars):
    expected = {
        "this_one": "/a/b/c/this_one.nl",
        "this_two": "/a/b/c/this_two.nl",
    }
    actual = dict_namelists_in_work_dir()
    assert expected == actual


def test_use_facet_as_key(path_to_mock_yaml_list, path_to_kgo_yaml_dict):
    # Copy known input to a temp file
    with tempfile.NamedTemporaryFile() as tmp:
        shutil.copyfile(path_to_mock_yaml_list, tmp.name)

        # The filepath is given by .name
        use_facet_as_key(str(tmp.name))

        # Read the result
        tmp.seek(0)
        actual = yaml.safe_load(tmp)

    # Load the expected output
    with open(path_to_kgo_yaml_dict, "r") as file_handle:
        expected = yaml.safe_load(file_handle)

    assert actual == expected
