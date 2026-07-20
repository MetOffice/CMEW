# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.yml
    input for test_create_request
"""
from pathlib import Path
import configparser
from create_request_file import create_request, list_streams


def test_list_streams():
    mock_stream_dict = {
        "abc": [
            "Amon/abcd",
            "Aday/efgh",
        ],
        "def": [
            "SImon/ijkl",
        ],
        "xyz/grid-A": [
            "Omon/mnop",
        ],
    }
    expected = "abc def xyz"
    actual = list_streams(mock_stream_dict)
    assert actual == expected


def test_create_request(monkeypatch):
    monkeypatch.setenv(
        "DATASETS_LIST_DIR",
        str(Path(__file__).parent.parent.parent / "unittest" / "mock_data"),
    )
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_path = "/path/to/variables.txt"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    stream_id = "apm inm"

    monkeypatch.setenv("RAW_DATA_DIR_MODE", "use_saved")
    monkeypatch.setenv("ROOT_PROC_DIR", root_proc_dir)
    monkeypatch.setenv("ROOT_DATA_DIR", root_data_dir)
    monkeypatch.setenv("VARIABLES_PATH", variables_path)
    monkeypatch.setenv("MIP_TABLE_DIR", mip_table_dir)
    monkeypatch.setenv("STREAM_ID", stream_id)

    mock_request_defaults = {
        "metadata": {
            "base_date": "1850-01-01T00:00:00",
            "branch_method": "no parent",
            "license": (
                "GCModelDev model data is licensed under the "
                "Open Government License v3 "
                "(https://www.nationalarchives.gov.uk/"
                "doc/open-government-licence/version/3/)"
            ),
            "mip": "ESMVal",
            "mip_era": "GCModelDev",
            "model_type": "AGCM AER",
        },
        "common": {
            "mode": "relaxed",
            "package": "round-1",
        },
        "data": {
            "mass_data_class": "crum",
            "model_workflow_branch": "trunk",
            "model_workflow_revision": "not used except with data request",
        },
        "misc": {
            "atmos_timestep": 1200,
        },
        "conversion": {
            "mip_convert_plugin": "HadGEM3",
            "skip_archive": True,
            "cylc_args": "--no-detach -v",
        },
    }

    actual_request = create_request("u-cw673", mock_request_defaults)
    cfg = configparser.ConfigParser()
    cfg.read_dict(actual_request)
    actual = {section: dict(cfg[section]) for section in cfg.sections()}

    expected_request = str(
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "request_u-cw673.cfg"
    )
    config = configparser.ConfigParser()
    config.read(expected_request)
    expected = {
        section: dict(config[section]) for section in config.sections()
    }

    assert actual == expected
