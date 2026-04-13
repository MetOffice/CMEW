# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.

import os

from create_request_file import create_request, load_request_defaults


def test_create_request(monkeypatch):
    # Note that this test only works within the workflow due to the
    # following environment variable use. For command line pytest use, export
    # CYLC_WORKFLOW_RUN_DIR to point to a previous workflow run dir, or
    # workflow source dir.
    request_defaults_path = os.path.join(
        os.environ.get("CYLC_WORKFLOW_RUN_DIR"),
        "app/configure_standardise/etc/request_defaults.cfg",
    )

    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("CALENDAR", "360_day")
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("ROOT_PROC_DIR", "/path/to/proc/dir/")
    monkeypatch.setenv("ROOT_DATA_DIR", "/path/to/data/dir/")
    monkeypatch.setenv("SUITE_ID", "u-az513")
    monkeypatch.setenv("VARIABLES_PATH", "/path/to/variables.txt")
    monkeypatch.setenv("VARIANT_LABEL", "r1i1p1f1")
    monkeypatch.setenv("REQUEST_DEFAULTS_PATH", str(request_defaults_path))

    config = create_request()
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }

    request_defaults = load_request_defaults()
    expected = {}
    for section in request_defaults.sections():
        expected[section] = dict(request_defaults.items(section))

    expected["metadata"].update(
        {
            "calendar": "360_day",
            "institution_id": "MOHC",
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
        }
    )
    expected["common"].update(
        {
            "mip_table_dir": os.path.expanduser(
                expected["common"]["mip_table_dir"]
            ),
            "root_proc_dir": "/path/to/proc/dir/",
            "root_data_dir": "/path/to/data/dir/",
            "workflow_basename": "u-az513",
        }
    )
    expected["data"].update(
        {
            "start_date": "1993-01-01T00:00:00",
            "end_date": "1994-01-01T00:00:00",
            "model_workflow_id": "u-az513",
            "variable_list_file": "/path/to/variables.txt",
        }
    )

    assert actual == expected
