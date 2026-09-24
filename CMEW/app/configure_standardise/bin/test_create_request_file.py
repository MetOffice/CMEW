# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.yml
    input for test_create_request
"""
import configparser
import create_request_file
from configure_standardise_conftest import (
    model_runs_yml_fp,
    request_u_cw673_cfg_fp,
)


def fake_list_streams(*args):
    return "apm inm"


def test_create_request(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    dataset = "u-cw673"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_path = "/path/to/variables.txt"
    raw_data_dir_mode = "use_saved"

    mock_request_defaults = {
        "metadata": {
            "base_date": "1850-01-01T00:00:00",
            "branch_method": "no parent",
            "license": (
                "GCModelDev model data is licensed under the "
                "Open Government License v3 "
                "(https://www.nationalarchives.gov.uk/"
                "doc/open-government-licence/version/3/)"
            ),
            "mip": "ESMVal",
            "mip_era": "GCModelDev",
            "model_type": "AGCM AER",
        },
        "common": {
            "mode": "relaxed",
            "package": "round-1",
        },
        "data": {
            "mass_data_class": "crum",
            "model_workflow_branch": "trunk",
            "model_workflow_revision": "not used except with data request",
        },
        "misc": {
            "atmos_timestep": 1200,
        },
        "conversion": {
            "mip_convert_plugin": "HadGEM3",
            "skip_archive": True,
            "cylc_args": "--no-detach -v",
        },
        "netcdf_global_attributes": {
            "further_info_url": "dummy_url",
        },
    }

    actual_request = create_request_file.create_request(
        dataset,
        mip_table_dir,
        str(model_runs_yml_fp()),
        root_proc_dir,
        root_data_dir,
        variables_path,
        raw_data_dir_mode,
        mock_request_defaults,
    )
    cfg = configparser.ConfigParser()
    cfg.read_dict(actual_request)
    actual = {section: dict(cfg[section]) for section in cfg.sections()}

    expected_request = str(request_u_cw673_cfg_fp())
    config = configparser.ConfigParser()
    config.read(expected_request)
    expected = {
        section: dict(config[section]) for section in config.sections()
    }

    assert actual == expected
