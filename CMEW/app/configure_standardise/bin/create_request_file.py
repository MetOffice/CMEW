#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request configuration file from the ESMValTool recipe.
"""
import configparser
import os
from pathlib import Path


def create_request():
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration.
    """
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    request = configparser.ConfigParser()
    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": os.environ["CALENDAR"],
        "experiment_id": os.environ["EXP_TYPE"],
        "institution_id": os.environ["INSTITUTION_ID"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": os.environ["MODEL_ID"],
        "model_type": "AGCM AER",
        "sub_experiment_id": "none",
        "variant_label": os.environ["VARIANT_LABEL"],
    }
    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": os.environ["SUITE_ID"],
    }
    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": os.environ["SUITE_ID"],
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{os.environ['START_YEAR']}-01-01T00:00:00",
        "streams": "apm",
        "variable_list_file": os.environ["VARIABLES_PATH"],
    }
    request["misc"] = {
        "atmos_timestep": "1200",
    }
    request["conversion"] = {
        "mip_convert_plugin": "UKESM1",
        "skip_archive": "True",
        "cylc_args": "--no-detach -v",
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
    target_path = Path(os.environ["REQUEST_PATH"])
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
