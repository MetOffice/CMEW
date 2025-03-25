# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
import json
import pytest
from create_request_file import make_request_file

# Testing app/configure_standardise/bin/create_request_file.py
# To see the request file produced, run pytest from CMEW with the arguments:
# CMEW/app/configure_standardise/bin/test_create_request_file.py -s

model_id = "UKESM1-0-LL"
suite_id = "u-az513"
calendar = "360_day"
variant_label = "r1i1p1f1"
test_file = "request.json"  # Result file


@pytest.fixture
def monkey_env(monkeypatch):
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("START_YEAR", "1993")


@pytest.fixture
def request_file_path(tmp_path):
    # path to new result file
    filepath = tmp_path / test_file
    return filepath


def test_create_request(monkey_env, request_file_path):  # noqa : 36
    # Create a CDDS request file and compare it to the expected result file.
    # The result file path is not printed by default if they match, but will be
    # shown by pytest <file> -s .
    # noqa : 36 : Ignore warning about monkey_env not being used; it is used
    # silently but not referenced.

    request = make_request_file(
        request_file_path, model_id, suite_id, calendar, variant_label
    )
    assert request is not None, "Request was not produced"
    print(f"\nRequest file:\n{request_file_path}")

    actual = read_file(request_file_path)
    assert actual == expected_request()


def read_file(request_file_path):
    # read the file produced
    with open(request_file_path, "r") as file:
        data = json.load(file)
    return data


def expected_request():
    expected = {
        "atmos_timestep": "1200",
        "branch_method": "no parent",
        "calendar": calendar,
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
        "model_id": model_id,
        "model_type": "AGCM AER",
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "run_bounds_for_stream_apm": "1993-01-01T00:00:00 1994-01-01T00:00:00",
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": suite_id,
        "suite_revision": "not used except with data request",
        "variant_label": variant_label,
    }
    return expected
