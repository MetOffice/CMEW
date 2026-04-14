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
    """
    Load default values for request file.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration default settings.
    """
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
    defaults = load_request_defaults()

    mip_table_dir = os.environ["MIP_TABLE_DIR"]
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    request = configparser.ConfigParser()
    request["metadata"] = {
        **defaults["metadata"],
        "calendar": os.environ["CALENDAR"],
        "experiment_id": os.environ["EXPERIMENT_ID"],
        "institution_id": os.environ["INSTITUTION_ID"],
        "model_id": os.environ["MODEL_ID"],
        "sub_experiment_id": os.environ["SUITE_ID"].replace("-", ""),
        "variant_label": os.environ["VARIANT_LABEL"],
    }
    request["common"] = {
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": os.environ["SUITE_ID"],
    }
    request["data"] = {
        **defaults["data"],
        "end_date": f"{end_year}-01-01T00:00:00",
        "model_workflow_id": os.environ["SUITE_ID"],
        "start_date": f"{os.environ['START_YEAR']}-01-01T00:00:00",
        # For now there is only one stream, for Amon and Emon mip.
        "streams": os.environ["STREAM_ID"],
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
