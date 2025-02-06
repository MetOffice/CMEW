# (C) British Crown Copyright 2024-2025, Met Office.
# Please see LICENSE for license details.
from create_request_file import create_request


def test_create_request(monkeypatch):
    monkeypatch.setenv("CALENDAR", "360_day")
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("SUITE_ID", "u-az513")

    actual = create_request()
    expected = {
        "atmos_timestep": "1200",
        "branch_method": "no parent",
        "calendar": "360_day",
        "child_base_date": "1850-01-01T00:00:00",
        "config_version": "1.0.1",
        "experiment_id": "amip",
        "external_plugin": "",
        "external_plugin_location": "",
        "global_attributes": {},
        "institution_id": "MOHC",
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mass_data_class": "crum",
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "mip_table_dir": "/home/h03/cdds/etc/mip_tables/GCModelDev/0.0.9",
        "model_id": "UKESM1-0-LL",
        "model_type": "AGCM AER",
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "run_bounds_for_stream_apm": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": "u-az513",
        "suite_revision": "not used except with data request",
        "variant_label": "r1i1p1f1",
    }
    assert actual == expected
