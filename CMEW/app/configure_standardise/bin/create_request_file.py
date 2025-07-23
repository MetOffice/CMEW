#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request.json file from the ESMValTool recipe.
"""
import configparser
import os
from pathlib import Path


def create_request():
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
    dict
        CDDS request information to be written to JSON file.
    """
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    request = configparser.ConfigParser()
    request["metadata"] = {
        "branch_method": "no parent",
        "calendar": os.environ["CALENDAR"],
        "base_date": "1850-01-01T00:00:00",
        "experiment_id": "amip",
        "institution_id": os.environ["INSTITUTION_ID"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": os.environ["MODEL_ID"],
        "model_type": "AGCM AER",
        "sub_experiment_id": "none",
        "variant_label": "r1i1p1f1",
    }
    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.9"
        ),
        "package": "round-1",
        "workflow_basename": "CMEW",
    }
    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": os.environ["SUITE_ID"],
        "model_workflow_revision": "not used except with data request",
        "streams": "apm",
        "start_date": f"{os.environ['START_YEAR']}-01-01T00:00:00",
    }
    request["misc"] = {
        "atmos_timestep": "1200",
    }
    return request


def write_request(request, target_path):
    """Write the request configuration to a file at ``target_path``.

    Parameters
    ----------
    request : configparser.ConfigParser()
        The request configuration.

    target_path: Path
        The full path to the file
        where the request configuration will be written.
    """
    with open(target_path, mode="w") as file_handle:
        request.write(file_handle)


def main():
    target_path = (
        Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "etc" / "request.json"
    )
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
