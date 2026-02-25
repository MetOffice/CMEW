# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
from create_request_file import load_request_defaults
import os
from create_request_file import create_request


def expected_request():
    """Return the expected request."""

    request_defaults = load_request_defaults()
    expected = {}
    for section in request_defaults.sections():
        expected[section] = dict(request_defaults.items(section))

    # Match runtime behaviour
    expected["common"]["mip_table_dir"] = os.path.expanduser(
        expected["common"]["mip_table_dir"]
    )

    return expected


def test_create_request(monkeypatch):
    # In the order defined in 'create_request_file.py'.
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

    config = create_request()
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }
    expected = expected_request()

    assert actual == expected
