#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request configuration file from the ESMValTool recipe.
"""
import configparser
import os
from pathlib import Path


def load_request_defaults():
    cfg = configparser.ConfigParser()
    cfg.read(os.environ.get("REQUEST_DEFAULTS_PATH"))

    return cfg


def create_request():
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration.
    """
<<<<<<< 209_config_cdds_dafault_request_items

    defaults = load_request_defaults()
    start_year = int(os.environ["START_YEAR"])
=======
    mip_table_dir = os.environ["MIP_TABLE_DIR"]

>>>>>>> main
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    request = configparser.ConfigParser()
    request["metadata"] = {
        **defaults["metadata"],
        "calendar": os.environ["CALENDAR"],
<<<<<<< 209_config_cdds_dafault_request_items
=======
        "experiment_id": os.environ["EXPERIMENT_ID"],
>>>>>>> main
        "institution_id": os.environ["INSTITUTION_ID"],
        "model_id": os.environ["MODEL_ID"],
<<<<<<< 209_config_cdds_dafault_request_items
=======
        "model_type": "AGCM AER",
        "sub_experiment_id": os.environ["SUITE_ID"].replace("-", ""),
>>>>>>> main
        "variant_label": os.environ["VARIANT_LABEL"],
    }

    request["common"] = {
<<<<<<< 209_config_cdds_dafault_request_items
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(
            defaults["common"]["mip_table_dir"]
        ),
=======
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "mode": "relaxed",
        "package": "round-1",
>>>>>>> main
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": os.environ["SUITE_ID"],
    }
    request["data"] = {
        **defaults["data"],
        "start_date": f"{start_year}-01-01T00:00:00",
        "end_date": f"{end_year}-01-01T00:00:00",
        "model_workflow_id": os.environ["SUITE_ID"],
<<<<<<< 209_config_cdds_dafault_request_items
=======
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{os.environ['START_YEAR']}-01-01T00:00:00",
        # For now there is only one stream, for Amon and Emon mip.
        "streams": os.environ["STREAM_ID"],
>>>>>>> main
        "variable_list_file": os.environ["VARIABLES_PATH"],
    }
    request["misc"] = dict(defaults["misc"])
    request["conversion"] = dict(defaults["conversion"])
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
