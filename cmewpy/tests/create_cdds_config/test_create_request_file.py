# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for create_request_file.
"""
import os

from cmewpy.create_cdds_config import create_request_file
from cmewpy.create_cdds_config.config_create_cdds_config import (
    request_defaults,
)


def fake_list_streams(*args):
    return "apm inm"


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
    cdds_run_identifier = "CMEW_run1"

    actual = create_request_file.create_request(
        mip_table_dir,
        dataset_metadata,
        root_proc_dir,
        root_data_dir,
        variables_file,
        raw_data_dir_mode,
        cdds_run_identifier,
        request_defaults,
    )
    expected = {
        "common": {
            "mip_table_dir": os.path.expanduser(mip_table_dir),
            "mode": "relaxed",
            "package": "round-1",
            "root_data_dir": root_data_dir,
            "root_proc_dir": root_proc_dir,
            "workflow_basename": f"{cdds_run_identifier}_{suite_id}",
        },
        "conversion": {
            "cylc_args": "--no-detach -v",
            "mip_convert_plugin": "HadGEM3",
            "skip_archive": True,
            "skip_extract": True,
        },
        "data": {
            "end_date": f"{end_year+1}-01-01T00:00:00",
            "mass_data_class": "crum",
            "model_workflow_branch": "trunk",
            "model_workflow_id": suite_id,
            "model_workflow_revision": "not used except with data request",
            "start_date": f"{start_year}-01-01T00:00:00",
            "streams": "apm inm",
            "variable_list_file": variables_file,
        },
        "metadata": {
            "base_date": "1850-01-01T00:00:00",
            "branch_method": "no parent",
            "calendar": calendar,
            "experiment_id": experiment_id,
            "institution_id": institute,
            "license": (
                "GCModelDev model data is licensed under the "
                "Open Government License v3 "
                "(https://www.nationalarchives.gov.uk/"
                "doc/open-government-licence/version/3/)"
            ),
            "mip": "ESMVal",
            "mip_era": "GCModelDev",
            "model_id": model_id,
            "model_type": "AGCM AER",
            "variant_label": variant_label,
        },
        "misc": {
            "atmos_timestep": 1200,
        },
        "netcdf_global_attributes": {
            "further_info_url": "dummy_url",
        },
    }
    assert actual == expected
