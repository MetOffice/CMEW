from add_datasets_to_share import extract_sections_from_naml, convert_str_to_facets, add_common_facets, process_naml_file, write_dict_to_yaml, write_datasets_to_yaml, dict_namelists_in_grandparent_dir
from pathlib import Path
import pytest
import yaml
import tempfile
import unittest
from unittest.mock import patch
import sys
import os


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "10")


@pytest.fixture
def path_to_kgo_yaml():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "test_model_runs.yml"
    )
    return str(path)


@pytest.fixture
def path_to_mock_nl():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "test_model_runs.nl"
    )
    return str(path)


@pytest.fixture
def path_to_kgo_dict():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "kgo_test_dict.yml"
    )
    return path


def test_extract_sections_from_naml(path_to_mock_nl):
    expected = [
        "calendar=gregorian,label_for_plots=HadGEM3-GC5E-LL N96ORCA1,model_id=HadGEM3-GC5E-LL,suite_id=u-cw673,variant_label=r1i1p1f1,",
        "calendar=360_day,label_for_plots=HadGEM3-GC3.1 N96ORCA1,model_id=HadGEM3-GC31-LL,suite_id=u-bv526,variant_label=r5i1p1f3,"
    ]

    actual = extract_sections_from_naml(path_to_mock_nl)
    assert actual == expected


def test_convert_str_to_facets():
    section = "calendar=gregorian,label_for_plots=HadGEM3-GC5E-LL N96ORCA1,model_id=HadGEM3-GC5E-LL,suite_id=u-cw673,variant_label=r1i1p1f1,"
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
            'calendar': 'gregorian',
            'label_for_plots': 'HadGEM3-GC5E-LL N96ORCA1',
            'model_id': 'HadGEM3-GC5E-LL',
            'suite_id': 'u-cw673',
            'variant_label': 'r1i1p1f1',
            'start_year': 1993,
            'end_year': 2002,
            'project': 'CMIP6'
         },
        {
            'calendar': '360_day',
            'label_for_plots': 'HadGEM3-GC3.1 N96ORCA1',
            'model_id': 'HadGEM3-GC31-LL',
            'suite_id': 'u-bv526',
            'variant_label': 'r5i1p1f3',
            'start_year': 1993,
            'end_year': 2002,
            'project': 'CMIP6'
        }
    ]

    actual = process_naml_file(path_to_mock_nl)
    assert actual == expected


# This one was only *some* random copying of Google
def test_write_dict_to_yaml(path_to_kgo_dict):
    # Note the keys are not alphabetical here but are in the output
    test_dict = {
        "key_1": "value_1",
        "key_for_list": [
            "item_1",
            "item_2",
            "item_3"
        ],
        "key_for_dict": {
            "nested_key_1": "nested_value_1",
            "nested_key_2": "nested_value_2"
        }
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
def test_write_datasets_to_yaml(monkeypatch):
    def mock_write_dict_to_yaml(dict_to_write, target_path):
        return target_path

    monkeypatch.setattr("add_datasets_to_share.write_dict_to_yaml", mock_write_dict_to_yaml)

    result = write_datasets_to_yaml({"a": 1}, "test_name", "/tmp")
    assert result == "/tmp/test_name.yml"


# This was a massive mess of Googling / trawling Stack Exchange.
# Please do tell me if it's not right / there are better ways.
class TestDictNamelistsInGrandparentDir(unittest.TestCase):
    @patch.object(sys.modules[__name__], "__file__", "/a/b/c/d/e.py")
    def test_directory_is_grandparent(self):
        assert os.path.dirname(os.path.dirname(__file__)) == "/a/b/c"

    @patch("os.path.dirname", return_value="/a/b/c")
    @patch("os.listdir", return_value=["this_one.nl", "this_two.nl", "not_this_one.txt", "subdir"])
    def test_only_nl_files_listed(self, mock_dirname, mock_listdir):
        expected = {
            "this_one": "/a/b/c/this_one.nl",
            "this_two": "/a/b/c/this_two.nl"
        }
        actual = dict_namelists_in_grandparent_dir()
        assert expected == actual
