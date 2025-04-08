#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request.json file from the ESMValTool recipe.
"""
import os
from pathlib import Path
import json


def create_request():
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
    dict
        CDDS request information to be written to JSON file.
    """
    streams = ["apm"]
    start_datetime = f"{os.environ['START_YEAR']}-01-01T00:00:00"
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    end_datetime = f"{end_year}-01-01T00:00:00"
    run_bounds = f"{start_datetime} {end_datetime}"
    streams_run_bounds = {
        f"run_bounds_for_stream_{stream}": run_bounds for stream in streams
    }
    request = {
        "atmos_timestep": "1200",
        "branch_method": "no parent",
        "calendar": os.environ["CALENDAR"],
        "child_base_date": "1850-01-01T00:00:00",
        "config_version": "1.0.1",
        "experiment_id": "amip",
        "external_plugin": "",
        "external_plugin_location": "",
        "global_attributes": {},
        "institution_id": os.environ["INSTITUTION_ID"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mass_data_class": "crum",
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.9"),
        "model_id": os.environ["MODEL_ID"],
        "model_type": "AGCM AER",
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": run_bounds,
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": os.environ["SUITE_ID"],
        "suite_revision": "not used except with data request",
        "variant_label": "r1i1p1f1",
    }
    # Combine request dict and streams_run_bounds dict (in-place union).
    request |= streams_run_bounds
    return request


def write_request(request, target_path):
    """Write request dictionary to a JSON file at ``target_path``.

    Parameters
    ----------
    request : dict
        Dictionary containing the request information.

    target_path: Path
        Location to write the request file.
    """
    with open(target_path, mode="w") as file:
        json.dump(request, file, separators=(",\n", ": "))


def main():
    target_path = (
        Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "etc" / "request.json"
    )
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
