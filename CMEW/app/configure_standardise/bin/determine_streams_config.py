#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Determines the stream config used to create the request and variables files.
"""
import os
import sys
import yaml
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def determine_stream_config_fp():
    """
    Provide a path to pp file stream configuration data.

    Uses the value of key `use_custom_data_streams` in the dataset information,
    and returns either `path_to_custom_streams_config` or a default value.
    The dataset is determined by variable `CYLC_TASK_PARAM_dataset`.

    Returns
    -------
    str
        Filepath to stream information for the dataset.
    """
    # Load the dataset information from model_runs YAML
    dataset = os.environ["CYLC_TASK_PARAM_dataset"].strip()
    with open(os.environ["MODEL_RUNS_CONFIG"]) as f:
        content = yaml.safe_load(f)
    dataset_dict = content[dataset]
    logger.debug("Dataset information:\n%s", dataset_dict)

    # Check whether a custom stream map is set to be used
    if dataset_dict.get("use_custom_data_streams") == True:
        streams_config = dataset_dict["path_to_custom_streams_config"]
    else:
        streams_config = os.environ["DEFAULT_STREAM_CONFIG_PATH"]
    logger.info(
        "Stream info for dataset % will use: %s", dataset, streams_config
    )

    return streams_config
