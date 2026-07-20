#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration file.
"""
import configparser
import importlib
import os
import sys
from pathlib import Path
import yaml
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def load_request_defaults(request_defaults_file):
    """
    Load default values for request file.

    Parameters
    ----------
    request_defaults_file : str
        The name of a python file in the same directory
        containing the CDDS request default values.

    Returns
    -------
    dict
        CDDS request configuration default settings.
    """
    # Load the CDDS default values
    module = importlib.import_module(request_defaults_file)
    config = module.request_defaults
    logger.debug(
        "Default config:\n%s",
        config,
    )
    return config


def list_streams(stream_info_file):
    """
    Lists all streams in the streams_config.py file.

    Parameters
    ----------
    stream_info_file : str
        The name of a python file in the same directory
        containing information about data streams.

    Returns
    -------
    str
        Space separated list of all streams.
    """
    # Load the stream information dictionary
    module = importlib.import_module(stream_info_file)
    config = module.streams_dict
    logger.debug("Stream information:\n%s", config)

    # List all streams (keys)
    all_streams = []
    for stream in config:
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


def create_request(model_run, request_defaults_file, stream_info_file):
    """
    Build a CDDS request configuration for a run identified by a suite_id.

    Uses information from the model_runs.yml file.

    Parameters
    ----------
    model_run : str
        The suite ID as a model run identifier.
    request_defaults_file : str
        The name of a python file in the same directory
        containing the CDDS request default values.
    stream_info_file : str
        The name of a python file in the same directory
        containing information about data streams.

    Returns
    -------
    dict
        CDDS request configuration.
    """
    defaults = load_request_defaults(request_defaults_file)

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
        "streams": list_streams(stream_info_file),
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

    request = create_request(
        dataset, "request_defaults_config", "streams_config"
    )
    target_path = Path(os.environ["REQUEST_PATH"])
    write_request(request, target_path)


if __name__ == "__main__":
    main()
