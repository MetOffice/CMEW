#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration file.
"""
import configparser
import os
import sys
from pathlib import Path
import yaml
import logging
from config import requests_defaults, streams_dict

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def list_streams(stream_dict=streams_dict):
    """
    Lists all streams in the streams_config.py file.

    Parameters
    ----------
    stream_dict : dict
        A dictionary containing information about data streams.

    Returns
    -------
    str
        Space separated list of all streams.
    """
    # Load the stream information dictionary
    logger.debug("Stream information:\n%s", stream_dict)

    # List all streams (keys)
    all_streams = []
    for stream in stream_dict:
        # For substreams we only want the first part
        stream = stream.split("/")[0]
        all_streams.append(stream)

    # Return as a space separated list
    stream_str = " ".join(all_streams)
    logger.debug(
        "Stream string:\n%s",
        stream_str,
    )

    return stream_str


def create_request(model_run, request_defaults=requests_defaults):
    """
    Build a CDDS request configuration for a run identified by a suite_id.

    Uses information from the model_runs.yml file.

    Parameters
    ----------
    model_run : str
        The suite ID as a model run identifier.
    request_defaults : dict
        A dictionary containing the CDDS request default values.

    Returns
    -------
    dict
        CDDS request configuration.
    """
    defaults = request_defaults

    mip_table_dir = os.environ["MIP_TABLE_DIR"]

    # Read the model run information from the model_runs.yml file
    model_runs_yaml = Path(os.environ["DATASETS_LIST_DIR"]) / "model_runs.yml"
    with open(model_runs_yaml, "r") as f:
        dataset_dict = yaml.safe_load(f)[model_run]
    logger.debug(
        "Dataset % config:\n%s",
        model_run,
        dataset_dict,
    )

    # Create the CDDS request
    request = {}
    request["metadata"] = {
        **defaults["metadata"],
        "base_date": defaults["metadata"]["base_date"],
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
        "start_date": f"{dataset_dict['start_year']}-01-01T00:00:00",
        "end_date": f"{int(dataset_dict['end_year'])+1}-01-01T00:00:00",
        "model_workflow_id": dataset_dict["suite_id"],
        # List all possible streams as CDDS just ignores ones without variables
        "streams": list_streams(),
        "variable_list_file": os.environ["VARIABLES_PATH"],
    }
    request["misc"] = dict(defaults["misc"])
    request["conversion"] = dict(defaults["conversion"])
    if os.environ["RAW_DATA_DIR_MODE"] == "use_saved":
        request["conversion"]["skip_extract"] = "True"

    logger.debug("Request config:\n%s", request)
    return request


def write_request(request, target_path):
    """Write the request configuration to a file at ``target_path``.

    Parameters
    ----------
    request : dict
        The request configuration.

    target_path: Path
        The full path to the file
        where the request configuration will be written.
    """
    cfg = configparser.ConfigParser()
    cfg.read_dict(request)

    logger.debug("Writing request config:\n%s", cfg)

    with open(target_path, mode="w") as file_handle:
        cfg.write(file_handle)


def main():
    """
    Generate and write the request file for the current task environment.

    The output file location is taken from the REQUEST_PATH environment
    variable. All other required inputs are read from the environment
    by ``create_request()``.
    """
    dataset = os.environ["CYLC_TASK_PARAM_dataset"].strip()
    logger.info("Creating CDDS request for dataset %s", dataset)

    request = create_request(dataset)
    target_path = Path(os.environ["REQUEST_PATH"])
    write_request(request, target_path)


if __name__ == "__main__":
    main()
