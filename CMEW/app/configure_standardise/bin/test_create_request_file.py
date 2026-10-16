# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for create_request_file.
"""
from pathlib import Path

import create_request_file
from config_configure_standardise import request_defaults


def fake_list_streams(*args):
    return "apm inm"


def test_external_mapping_plugin_location(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    request = create_request_file.create_request(
        "/path/to/mip_tables",
        {
            "calendar": "360_day",
            "experiment_id": "amip",
            "institute": "MOHC",
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "suite_id": "u-ds902",
            "start_year": 3150,
            "end_year": 3159,
        },
        "/path/to/proc",
        "/path/to/data",
        "/path/to/variables.txt",
        "off",
        request_defaults,
    )

    assert request["conversion"]["mip_convert_plugin"] == "UKESM1"
    assert request["conversion"]["mip_convert_external_plugin"] == (
        "cmew_ukesm1_plugin"
    )
    assert request["conversion"]["mip_convert_external_plugin_location"] == (
        str(Path(create_request_file.__file__).resolve().parent)
    )
    assert request["common"]["mip_table_dir"] == (
        "/data/scratch/jonathan.lillis/mip_tables/0.0.25/"
    )


def test_create_request(monkeypatch):
    monkeypatch.setattr(create_request_file, "list_streams", fake_list_streams)
    calendar = "gregorian"
    experiment_id = "amip"
    institute = "MOHC"
    model_id = "HadGEM3-GC5E-LL"
    variant_label = "r1i1p1f1"
    suite_id = "u-cw673"
    start_year = 1993
    end_year = 2003
    dataset_metadata = {
        "calendar": calendar,
        "experiment_id": experiment_id,
        "institute": institute,
        "model_id": model_id,
        "variant_label": variant_label,
        "suite_id": suite_id,
        "start_year": start_year,
        "end_year": end_year,
    }
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    variables_file = "/path/to/variables.txt"
    raw_data_dir_mode = "use_saved"

    actual = create_request_file.create_request(
        mip_table_dir,
        dataset_metadata,
        root_proc_dir,
        root_data_dir,
        variables_file,
        raw_data_dir_mode,
        request_defaults,
    )
    assert actual["common"]["mip_table_dir"] == (
        "/data/scratch/jonathan.lillis/mip_tables/0.0.25/"
    )
    assert actual["common"]["root_data_dir"] == root_data_dir
    assert actual["common"]["root_proc_dir"] == root_proc_dir
    assert actual["data"]["streams"] == "apm inm"
    assert actual["data"]["start_date"] == "1993-01-01T00:00:00"
    assert actual["data"]["end_date"] == "2004-01-01T00:00:00"
    assert actual["conversion"]["mip_convert_plugin"] == "UKESM1"
    assert actual["conversion"]["skip_qc"] is True
    assert actual["conversion"]["skip_extract"] is True
