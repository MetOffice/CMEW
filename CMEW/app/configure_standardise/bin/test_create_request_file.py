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
    request_defaults_yml_fp,
)


def fake_list_streams(*args):
    return "apm inm"


def test_external_mapping_plugin_location(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    defaults_path = request_defaults_yml_fp()
    request = create_request_file.create_request(
        str(defaults_path),
        "u-cw673",
        "/path/to/mip_tables",
        str(model_runs_yml_fp()),
        "/path/to/proc",
        "/path/to/data",
        "/path/to/variables.txt",
        "off",
    )

    assert request["conversion"]["mip_convert_plugin"] == "UKESM1"
    assert request["conversion"]["mip_convert_external_plugin"] == (
        "cmew_ukesm1_plugin"
    )
    assert request["conversion"]["mip_convert_external_plugin_location"] == (
        str(defaults_path.resolve().parent.parent / "bin")
    )


def test_create_request(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    dataset = "u-cw673"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_path = "/path/to/variables.txt"
    raw_data_dir_mode = "use_saved"

    actual_request = create_request_file.create_request(
        str(request_defaults_yml_fp()),
        dataset,
        mip_table_dir,
        str(model_runs_yml_fp()),
        root_proc_dir,
        root_data_dir,
        variables_path,
        raw_data_dir_mode,
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
