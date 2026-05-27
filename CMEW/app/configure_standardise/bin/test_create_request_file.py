# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.yml
    input for test_create_request
"""
import os
from pathlib import Path

from create_request_file import create_request, load_request_defaults


def test_create_request(monkeypatch):
    monkeypatch.setenv(
        "DATASETS_LIST_DIR",
        str(Path(__file__).parent.parent.parent / "unittest" / "mock_data"),
    )

    request_defaults_path = (
        Path(__file__).parent.parent / "etc" / "request_defaults.cfg"
    )
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_path = "/path/to/variables.txt"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    stream_id = "apm ap5 inm"

    monkeypatch.setenv("RAW_DATA_DIR_MODE", "use_saved")
    monkeypatch.setenv("REQUEST_DEFAULTS_PATH", str(request_defaults_path))
    monkeypatch.setenv("ROOT_PROC_DIR", root_proc_dir)
    monkeypatch.setenv("ROOT_DATA_DIR", root_data_dir)
    monkeypatch.setenv("VARIABLES_PATH", variables_path)
    monkeypatch.setenv("MIP_TABLE_DIR", mip_table_dir)
    monkeypatch.setenv("STREAM_ID", stream_id)

    config = create_request("u-cw673")
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }

    request_defaults = load_request_defaults()
    expected = {}
    for section in request_defaults.sections():
        expected[section] = dict(request_defaults.items(section))

    expected["metadata"] = {
        **request_defaults["metadata"],
        "calendar": "gregorian",
        "experiment_id": "amip",
        "institution_id": "MOHC",
        "model_id": "HadGEM3-GC5E-LL",
        "variant_label": "r1i1p1f1",
    }
    expected["common"] = {
        **request_defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": root_proc_dir,
        "root_data_dir": root_data_dir,
        "workflow_basename": "u-cw673",
    }
    expected["data"] = {
        **request_defaults["data"],
        "start_date": "1993-01-01T00:00:00",
        "end_date": "2003-01-01T00:00:00",
        "model_workflow_id": "u-cw673",
        "streams": stream_id,
        "variable_list_file": variables_path,
    }
    expected["conversion"] = {
        **request_defaults["conversion"],
        "skip_extract": "True",
    }

    assert actual == expected
