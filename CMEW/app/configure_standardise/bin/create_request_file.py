#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request configuration file from the ESMValTool recipe.
"""
import configparser
import os
from pathlib import Path


def load_defaults():
    cfg = configparser.ConfigParser()

    # 1. Explicit override (tests or power users)
    if "REQUEST_DEFAULTS_CFG" in os.environ:
        cfg_path = Path(os.environ["REQUEST_DEFAULTS_CFG"])

    # 2. Source tree (works for Cylc vip + pytest)
    else:
        # create_request_file.py → bin → configure_standardise
        cfg_path = (
            Path(__file__).resolve().parents[1]
            / "etc"
            / "request_defaults.cfg"
        )

    if not cfg_path.exists():
        raise FileNotFoundError(f"Defaults file not found: {cfg_path}")

    cfg.read(cfg_path)
    return cfg


def create_request():
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration.
    """

    defaults = load_defaults()
    start_year = int(os.environ["START_YEAR"])
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    request = configparser.ConfigParser()
    request["metadata"] = {
        **defaults["metadata"],
        "calendar": os.environ["CALENDAR"],
        "institution_id": os.environ["INSTITUTION_ID"],
        "model_id": os.environ["MODEL_ID"],
        "variant_label": os.environ["VARIANT_LABEL"],
    }

    request["common"] = {
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(
            defaults["common"]["mip_table_dir"]
        ),
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": os.environ["SUITE_ID"],
    }
    request["data"] = {
        **defaults["data"],
        "start_date": f"{start_year}-01-01T00:00:00",
        "end_date": f"{end_year}-01-01T00:00:00",
        "model_workflow_id": os.environ["SUITE_ID"],
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
