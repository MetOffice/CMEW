# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.yml
    input for test_create_request
"""
import os
import pytest
from pathlib import Path
import yaml
from create_request_file import create_request, load_request_defaults


@pytest.fixture
def path_to_kgo_request():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "request_u-cw673.cfg"
    )
    return path


def test_create_request(monkeypatch, path_to_kgo_request):
    monkeypatch.setenv(
        "DATASETS_LIST_DIR",
        str(Path(__file__).parent.parent.parent / "unittest" / "mock_data"),
    )

    request_defaults_path = (
        Path(__file__).parent.parent / "etc" / "request_defaults.yml"
    )
    stream_config_path = Path(__file__).parent.parent / "etc" / "streams.yml"
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_path = "/path/to/variables.txt"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    stream_id = "apm ap5 inm"

    monkeypatch.setenv("RAW_DATA_DIR_MODE", "use_saved")
    monkeypatch.setenv("REQUEST_DEFAULTS_PATH", str(request_defaults_path))
    monkeypatch.setenv("STREAM_CONFIG_PATH", str(stream_config_path))
    monkeypatch.setenv("ROOT_PROC_DIR", root_proc_dir)
    monkeypatch.setenv("ROOT_DATA_DIR", root_data_dir)
    monkeypatch.setenv("VARIABLES_PATH", variables_path)
    monkeypatch.setenv("MIP_TABLE_DIR", mip_table_dir)
    monkeypatch.setenv("STREAM_ID", stream_id)

    actual = create_request("u-cw673")
    with open(path_to_kgo_request, "r") as f:
        expected = yaml.safe_load(f)

    assert actual == expected
