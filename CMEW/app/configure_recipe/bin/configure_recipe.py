#!/usr/bin/env python
# (C) Crown Copyright 2022-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate the required user configuration file for ESMValTool.
"""

import os
import yaml
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def main():
    """
    Write the required user and developer configuration files for
    ESMValTool.
    """
    # Retrieve relevant environment variables
    values = retrieve_values_from_task_env()
    logger.info("Retrieving values")

    # Create a single configuration file
    user_config_path = values["USER_CONFIG_PATH"]
    logger.info("Creating user config")
    user_config_contents = create_user_config(values)

    # Write the file out
    ensure_parent_dir(user_config_path)
    logger.info("Writing user config to %s", user_config_path)
    write_yaml(user_config_path, user_config_contents)


def retrieve_values_from_task_env():
    """
    Return the values defined in the environment for the
    ``configure_recipe`` task.

    Returns
    -------
    : dictionary
        The values defined in the environment for the
        ``configure_recipe`` task.
    """
    values_from_task_env = {
        "CYLC_WORKFLOW_SHARE_DIR": os.environ["CYLC_WORKFLOW_SHARE_DIR"],
        "DEV_CONFIG_PATH": os.environ["DEV_CONFIG_PATH"],
        "MAX_PARALLEL_TASKS": os.environ["MAX_PARALLEL_TASKS"],
        "MIP_TABLE_DIR": os.environ["MIP_TABLE_DIR"],
        "OUTPUT_DIR": os.environ["OUTPUT_DIR"],
        "ROOTPATH_CMIP6": os.environ["ROOTPATH_CMIP6"],
        "ROOTPATH_OBS": os.environ["ROOTPATH_OBS"],
        "ROOTPATH_OBS4MIPS": os.environ["ROOTPATH_OBS4MIPS"],
        "USER_CONFIG_PATH": os.environ["USER_CONFIG_PATH"],
    }
    logger.debug("Retrieved values:\n%s", values_from_task_env)
    return values_from_task_env


def retrieve_default_values():



def create_user_config(values=None):
    """
    Return the contents of the user configuration file.

    Parameters
    ----------
    values : dict, optional
        The values to use for the user configuration file.

    Returns
    -------
    dict
        The contents of the user configuration file.
    """
    values = values or {}

    esmval = None
    if "CYLC_WORKFLOW_SHARE_DIR" in values:
        esmval = os.path.join(
            values["CYLC_WORKFLOW_SHARE_DIR"],
            "work",
            "GCModelDev",
        )
    logger.debug("esmval: %s", esmval)

    # Note that 'auxiliary_data_dir' and 'download_dir'
    # are set to empty values and cannot currently be
    # configured. However, 'download_dir' is used only when using the
    # automatic download feature via ESMValTool (which we do not intend
    # to use here).
    # 'auxiliary_data_dir' is used by some recipes to look for
    # additional datasets, so may need to be configured in the future.

    user_config_file_contents = {
        "max_parallel_tasks": max_parallel_tasks,
        "output_dir": values.get("OUTPUT_DIR"),

            "CMIP6": values.get("ROOTPATH_CMIP6"),
            "OBS": values.get("ROOTPATH_OBS"),
            "OBS4MIPs": values.get("ROOTPATH_OBS4MIPS"),
            "ESMVal": esmval,

    logger.debug("User config file contents:\n%s", user_config_file_contents)
    return user_config_file_contents


def ensure_parent_dir(file_path):
    """
    Create the parent directory for ``file_path`` if needed.
    """
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        logging.debug("Making directory %s", parent_dir)
        os.makedirs(parent_dir, exist_ok=True)


def write_yaml(file_path, contents):
    """
    Write ``contents`` to the YAML file at ``file_path``.

    Parameters
    ----------
    file_path : str
        The full path to the YAML file.
    contents : dict
        The contents to write.
    """
    with open(file_path, "w", encoding="utf-8") as file_handle:
        yaml.safe_dump(
            contents,
            file_handle,
            default_flow_style=False,
            sort_keys=False,
        )


if __name__ == "__main__":
    main()
