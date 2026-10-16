#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration file.
"""
import configparser
import os
import sys
import yaml
import logging
from config_configure_standardise import request_defaults

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def load_yaml(yaml_path):
    """
    Return the contents of the YAML file.

    Parameters
    ----------
    yaml_path : str
        The full path to the YAML file.

    Returns
    -------
    dict
        The contents of the YAML file.
    """
    with open(yaml_path, "r") as file_handle:
        contents = yaml.safe_load(file_handle)
    logger.debug(f"Contents of {yaml_path}: {contents}")
    return contents


def list_streams(variables_file):
    """
    Lists all streams from a single variables file.

    Parameters
    ----------
    variables_file: str
        The full path to the variables file.

    Returns
    -------
    str
        Space separated list of all streams.
    """
    # Read the stream mappings
    with open(variables_file, "r") as file_handle:
        variables = file_handle.readlines()
        logger.debug(
            "All variables:\n%s",
            variables,
        )

    # List all streams (keys)
    all_streams = []
    for line in variables:
        # Get the whole stream including substream
        whole_stream = line.strip().split(":")[-1]

        # But don't list the substream
        stream = whole_stream.split("/")[0]

        # Only add unique streams
        if stream not in all_streams:
            all_streams.append(stream)

    # Return as a space separated list
    stream_str = " ".join(all_streams)
    logger.debug(
        "Stream string:\n%s",
        stream_str,
    )

    return stream_str


def create_request(
    mip_table_dir,
    dataset_metadata,
    root_proc_dir,
    root_data_dir,
    variables_file,
    raw_data_dir_mode,
    request_defaults=request_defaults,
):
    """
    Return a CDDS request for a dataset.

    Parameters
    ----------
    mip_table_dir : str
        The path to the MIP table directory to use from CDDS.
    dataset_metadata : dict
        The metadata associated with the dataset.
    root_proc_dir : str
        The directory for use when processing data with CDDS.
    root_data_dir : str
        The root directory for CDDS to store data.
    variables_file : str
        The full path to the file containing
        the list of variables to be processed.
    raw_data_dir_mode : str
        Whether to save or reuse raw CDDS data files.
    request_defaults : dict
        A dictionary containing the CDDS request default values.

    Returns
    -------
    dict
        The CDDS request.
    """
    defaults = request_defaults

    # Create the CDDS request
    request = {}
    request["metadata"] = {
        **defaults["metadata"],
        "base_date": defaults["metadata"]["base_date"],
        "calendar": dataset_metadata["calendar"],
        "experiment_id": dataset_metadata["experiment_id"],
        "institution_id": dataset_metadata["institute"],
        "model_id": dataset_metadata["model_id"],
        "variant_label": dataset_metadata["variant_label"],
    }
    request["common"] = {
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": root_proc_dir,
        "root_data_dir": root_data_dir,
        "workflow_basename": dataset_metadata["suite_id"],
    }
    request["data"] = {
        **defaults["data"],
        "start_date": f"{dataset_metadata['start_year']}-01-01T00:00:00",
        "end_date": f"{int(dataset_metadata['end_year'])+1}-01-01T00:00:00",
        "model_workflow_id": dataset_metadata["suite_id"],
        "streams": list_streams(variables_file),
        "variable_list_file": variables_file,
    }
    request["misc"] = dict(defaults["misc"])
    request["conversion"] = dict(defaults["conversion"])
    if raw_data_dir_mode == "use_saved":
        request["conversion"]["skip_extract"] = True
    request["netcdf_global_attributes"] = dict(
        defaults["netcdf_global_attributes"]
    )

    logger.debug("Request config:\n%s", request)
    return request


def write_request(request, output_filepath):
    """Write the request configuration to a file at ``output_filepath``.

    Parameters
    ----------
    request : dict
        The request configuration.

    output_filepath: Path
        The full path to the file
        where the request configuration will be written.
    """
    cfg = configparser.ConfigParser()
    cfg.read_dict(request)

    logger.debug("Writing request config:\n%s", cfg)

    with open(output_filepath, mode="w") as file_handle:
        cfg.write(file_handle)


def create_request_file(
    dataset,
    output_filepath,
    mip_table_dir,
    model_runs_yml_fp,
    root_proc_dir,
    root_data_dir,
    variables_file,
    raw_data_dir_mode,
):
    """
    Create a request file to standardise model data with CDDS.

    Parameters
    ----------
    dataset : str
        The model run to be extracted from MASS and processed.
    output_filepath : str
        The full path to the file where the
        request configuration will be written.
    mip_table_dir : str
        The path to the MIP table directory to use from CDDS.
    model_runs_yml_fp : str
        The full path to the YAML file containing details of the model runs.
    root_proc_dir : str
        The directory for use when processing data with CDDS.
    root_data_dir : str
        The root directory for CDDS to store data.
    variables_file : str
        The full path to the file containing
        the list of variables to be processed.
    raw_data_dir_mode : str
        Whether to save or reuse raw CDDS data files.
    """
    logger.info("Creating CDDS request for dataset %s", dataset)

    all_dataset_metadata = load_yaml(model_runs_yml_fp)
    dataset_metadata = all_dataset_metadata[dataset]
    request = create_request(
        mip_table_dir,
        dataset_metadata,
        root_proc_dir,
        root_data_dir,
        variables_file,
        raw_data_dir_mode,
    )
    write_request(request, output_filepath)
