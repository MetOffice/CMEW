# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.

import os
from pathlib import Path

from create_request_file import create_request, load_request_defaults


def write_request_defaults(tmp_path: Path) -> Path:
    """Create a temporary request defaults config file."""
    request_defaults = tmp_path / "request_defaults.cfg"
    request_defaults.write_text(
        "\n".join(
            [
                "[metadata]",
                "calendar = gregorian",
                "institution_id = TEST",
                "model_id = TEST-MODEL",
                "variant_label = r1i1p1f1",
                "",
                "[common]",
                "mip_table_dir = ~/mip_tables",
                "root_proc_dir = /default/proc",
                "root_data_dir = /default/data",
                "workflow_basename = default-suite",
                "",
                "[data]",
                "start_date = 1990-01-01T00:00:00",
                "end_date = 1991-01-01T00:00:00",
                "model_workflow_id = default-suite",
                "variable_list_file = /default/variables.txt",
                "",
                "[misc]",
                "dummy_misc = value",
                "",
                "[conversion]",
                "dummy_conversion = value",
                "",
            ]
        )
    )
    return request_defaults


def expected_request():
    """Return the expected request."""
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

    return expected


def test_create_request(monkeypatch, tmp_path):
    request_defaults_path = write_request_defaults(tmp_path)

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
    expected = expected_request()

    assert actual == expected
