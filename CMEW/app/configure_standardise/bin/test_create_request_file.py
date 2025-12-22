# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.

import os
import pytest

from create_request_file import create_request


def _set_base_env(monkeypatch):
    """
    Set the base environment variables needed by create_request().
    In the order defined in 'create_request_file.py'.
    """
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("CALENDAR", "360_day")
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("ROOT_PROC_DIR", "/path/to/proc/dir/")
    monkeypatch.setenv("ROOT_DATA_DIR", "/path/to/data/dir/")
    monkeypatch.setenv("SUITE_ID", "u-az513")
    monkeypatch.setenv("VARIABLES_PATH", "/path/to/variables.txt")


def _clear_extract_env(monkeypatch):
    """Ensure EXTRACT/EXTRACT_DATA_PATH do not leak from the suite env."""
    monkeypatch.delenv("EXTRACT", raising=False)
    monkeypatch.delenv("EXTRACT_DATA_PATH", raising=False)


def test_create_request_default_extract(monkeypatch):
    """EXTRACT default (True) - no skip_extract, root_data_dir unchanged."""
    _clear_extract_env(monkeypatch)
    _set_base_env(monkeypatch)
    # Do not set EXTRACT or EXTRACT_DATA_PATH → EXTRACT defaults to True.

    config = create_request()
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }

    expected = {
        "metadata": {
            "branch_method": "no parent",
            "calendar": "360_day",
            "base_date": "1850-01-01T00:00:00",
            "experiment_id": "amip",
            "institution_id": "MOHC",
            "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
            "mip": "ESMVal",
            "mip_era": "GCModelDev",
            "model_id": "UKESM1-0-LL",
            "model_type": "AGCM AER",
            "sub_experiment_id": "none",
            "variant_label": "r1i1p1f1",
        },
        "common": {
            "external_plugin": "",
            "external_plugin_location": "",
            "mip_table_dir": os.path.expanduser(
                "~cdds/etc/mip_tables/GCModelDev/0.0.9"
            ),
            "mode": "relaxed",
            "package": "round-1",
            "root_proc_dir": "/path/to/proc/dir/",
            "root_data_dir": "/path/to/data/dir/",
            "workflow_basename": "CMEW",
        },
        "data": {
            "end_date": "1994-01-01T00:00:00",
            "mass_data_class": "crum",
            "model_workflow_branch": "trunk",
            "model_workflow_id": "u-az513",
            "model_workflow_revision": "not used except with data request",
            "start_date": "1993-01-01T00:00:00",
            "streams": "apm",
            "variable_list_file": "/path/to/variables.txt",
        },
        "misc": {
            "atmos_timestep": "1200",
        },
        "conversion": {
            "mip_convert_plugin": "UKESM1",
            "skip_archive": "True",
            "cylc_args": "--no-detach -v",
            # NOTE: no 'skip_extract' key when EXTRACT defaults to True
        },
    }

    assert actual == expected


def test_create_request_extract_false_with_path(monkeypatch):
    """EXTRACT=False + EXTRACT_DATA_PATH set →
    skip_extract + override root_data_dir."""
    _clear_extract_env(monkeypatch)
    _set_base_env(monkeypatch)
    monkeypatch.setenv("EXTRACT", "false")
    monkeypatch.setenv("EXTRACT_DATA_PATH", "/pre/extracted/data")

    config = create_request()
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }

    # Ensure skip_extract is set in [conversion]
    assert actual["conversion"]["skip_extract"] == "True"

    # Ensure root_data_dir is taken from EXTRACT_DATA_PATH, not ROOT_DATA_DIR
    assert actual["common"]["root_data_dir"] == "/pre/extracted/data"

    # Optional extra checks to ensure other keys unaffected:
    assert actual["common"]["root_proc_dir"] == "/path/to/proc/dir/"
    assert actual["conversion"]["mip_convert_plugin"] == "UKESM1"


def test_create_request_extract_false_without_path_raises(monkeypatch):
    """EXTRACT=False with no EXTRACT_DATA_PATH → fail with ValueError."""
    _clear_extract_env(monkeypatch)
    _set_base_env(monkeypatch)
    monkeypatch.setenv("EXTRACT", "false")
    # EXTRACT_DATA_PATH intentionally not set (or could set to empty)

    with pytest.raises(ValueError, match="EXTRACT=False"):
        create_request()
