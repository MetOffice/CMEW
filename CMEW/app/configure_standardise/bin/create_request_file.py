#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
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
    stream = os.environ["STREAM"]
    run_bounds_for_stream_key = f"run_bounds_for_stream_{stream}"
    run_bounds = f"{os.environ['START_DATETIME']} {os.environ['END_DATETIME']}"
    request = {
        "atmos_timestep": os.environ["ATMOS_TIMESTEP"],
        "branch_method": "no parent",
        "calendar": os.environ["CALENDAR"],
        "child_base_date": "1850-01-01T00:00:00",
        "config_version": "1.0.1",
        "experiment_id": os.environ["EXPERIMENT_ID"],
        "external_plugin": "",
        "external_plugin_location": "",
        "global_attributes": {},
        "institution_id": os.environ["INSTITUTION_ID"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mass_data_class": os.environ["MASS_DATA_CLASS"],
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "mip_table_dir": "/home/h03/cdds/etc/mip_tables/GCModelDev/0.0.9",
        "model_id": os.environ["MODEL_ID"],
        "model_type": os.environ["MODEL_TYPE"],
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": run_bounds,
        run_bounds_for_stream_key: run_bounds,
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": os.environ["SUITE_ID"],
        "suite_revision": "not used except with data request",
        "variant_label": os.environ["VARIANT_LABEL"],
    }
    return request


def write_request(request, target_path):
    """Write request dict to a JSON file in the installed workflow.

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
