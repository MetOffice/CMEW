# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for add_datasets_to_share.py

Test data files:
/app/unittest/mock_data/model_runs.yml
    input for test_create_request
"""
from pathlib import Path
import configparser
import create_request_file


def fake_list_streams(*args):
    return "apm inm"


etc_dir = Path(__file__).parent.parent / "etc"
mock_data_dir = Path(__file__).parent.parent.parent / "unittest" / "mock_data"
test_defaults_path = etc_dir / "request_defaults.yml"
dataset = "u-cw673"
mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
model_runs_yml_fp = mock_data_dir / "model_runs.yml"
root_proc_dir = "/path/to/proc/dir/"
root_data_dir = "/path/to/data/dir/"
variables_path = "/path/to/variables.txt"
raw_data_dir_mode = "use_saved"

kgo_dir = Path(__file__).parent.parent.parent / "unittest" / "kgo"
kgo_request_fp = kgo_dir / "request_u-cw673.cfg"


def test_create_request(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    actual_request = create_request_file.create_request(
        str(test_defaults_path),
        dataset,
        mip_table_dir,
        str(model_runs_yml_fp),
        root_proc_dir,
        root_data_dir,
        variables_path,
        raw_data_dir_mode,
    )
    cfg = configparser.ConfigParser()
    cfg.read_dict(actual_request)
    actual = {section: dict(cfg[section]) for section in cfg.sections()}

    expected_request = str(kgo_request_fp)
    config = configparser.ConfigParser()
    config.read(expected_request)
    expected = {
        section: dict(config[section]) for section in config.sections()
    }

    assert actual == expected
