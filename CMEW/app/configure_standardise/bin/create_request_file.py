#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration file.
"""
import configparser
import os
from pathlib import Path
import yaml


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


def create_request(model_run):
    """
    Build a CDDS request configuration for a run identified by a suite_id.

    Uses information from the model_runs.yml file.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration.
    """
    defaults = load_request_defaults()

    mip_table_dir = os.environ["MIP_TABLE_DIR"]

    # Read the model run information from the model_runs.yml file
    model_runs_yaml = Path(os.environ["DATASETS_LIST_DIR"]) / "model_runs.yml"
    with open(model_runs_yaml, "r") as f:
        dataset_dict = yaml.safe_load(f)[model_run]

    # Create the CDDS request
    request = configparser.ConfigParser()
    request["metadata"] = {
        **defaults["metadata"],
        "calendar": dataset_dict["calendar"],
        "experiment_id": dataset_dict["experiment_id"],
        "institution_id": dataset_dict["institute"],
        "model_id": dataset_dict["model_id"],
        "variant_label": dataset_dict["variant_label"],
    }
    request["common"] = {
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": dataset_dict["suite_id"],
    }
    request["data"] = {
        **defaults["data"],
        "end_date": f"{dataset_dict["end_year"]}-01-01T00:00:00",
        "model_workflow_id": dataset_dict["suite_id"],
        "start_date": f"{dataset_dict["start_year"]}-01-01T00:00:00",
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
    """
    Generate and write the request file for the current task environment.

    The output file location is taken from the REQUEST_PATH environment
    variable. All other required inputs are read from the environment
    by ``create_request()``.
    """
    dataset = os.environ["CYLC_TASK_PARAM_dataset"].strip()
    request = create_request(dataset)
    target_path = Path(os.environ["REQUEST_PATH"])
    write_request(request, target_path)


if __name__ == "__main__":
    main()
