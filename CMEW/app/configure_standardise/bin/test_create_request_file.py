# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os

from create_request_file import create_request


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

    # New: required to match developer config custom.cmor_path
    monkeypatch.setenv(
        "MIP_TABLE_DIR", "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    )

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
            "license": (
                "GCModelDev model data is licensed under "
                "the Open Government License v3 "
                "(https://www.nationalarchives.gov.uk/doc"
                "/open-government-licence/version/3/)"
            ),
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
                "~cdds/etc/mip_tables/GCModelDev/0.0.25"
            ),
            "mode": "relaxed",
            "package": "round-1",
            "root_proc_dir": "/path/to/proc/dir/",
            "root_data_dir": "/path/to/data/dir/",
            "workflow_basename": "u-az513",
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
        },
    }

    assert actual == expected
