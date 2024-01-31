# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
from create_request_file import create_request


def test_create_request(monkeypatch):
    monkeypatch.setenv("ATMOS_TIMESTEP", "1200")
    monkeypatch.setenv("CALENDAR", "360_day")
    monkeypatch.setenv("EXPERIMENT_ID", "historical")
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("MASS_DATA_CLASS", "crum")
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("MODEL_TYPE", "AOGCM AER")
    monkeypatch.setenv("START_DATETIME", "1993-01-01T00:00:00")
    monkeypatch.setenv("END_DATETIME", "1994-01-01T00:00:00")
    monkeypatch.setenv("STREAM", "apm")
    monkeypatch.setenv("SUITE_ID", "u-az513")
    monkeypatch.setenv("VARIANT_LABEL", "r5i1p1f3")

    actual = create_request()
    expected = {
        "atmos_timestep": "1200",
        "branch_method": "no parent",
        "calendar": "360_day",
        "child_base_date": "1850-01-01T00:00:00",
        "config_version": "1.0.1",
        "experiment_id": "historical",
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
        "model_type": "AOGCM AER",
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "run_bounds_for_stream_apm": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": "u-az513",
        "suite_revision": "not used except with data request",
        "variant_label": "r5i1p1f3",
    }
    assert actual == expected
