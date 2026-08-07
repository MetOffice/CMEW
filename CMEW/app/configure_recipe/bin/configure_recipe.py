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


def create_developer_config(
    mip_table_dir,
):
    """
    Return the contents of the developer configuration file.

    Parameters
    ----------
    mip_table_dir:
        The full path to the MIP tables root directory.

    Returns
    -------
    dict
        Developer configuration content.
    """
    developer_config_file_contents = {
        "custom": {
            "cmor_path": mip_table_dir,
        },
        "ESMVal": {
            "cmor_strict": True,
            "input_dir": {
                "default": "/",
                "BADC": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "DKRZ": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "ESGF": (
                    "{project}/{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "ETHZ": (
                    "{exp}/{mip}/{short_name}/{dataset}/" "{ensemble}/{grid}/"
                ),
                "SYNDA": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
            },
            "input_file": (
                "{short_name}_{mip}_{dataset}_{exp}_{ensemble}_{grid}*.nc"
            ),
            "output_file": (
                "{project}_{dataset}_{mip}_{exp}_{ensemble}_"
                "{short_name}_{grid}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "GCModelDev_",
        },
        "CMIP6": {
            "cmor_strict": True,
            "input_dir": {
                "default": "/",
                "BADC": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "DKRZ": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "ESGF": (
                    "{project}/{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "ETHZ": (
                    "{exp}/{mip}/{short_name}/{dataset}/" "{ensemble}/{grid}/"
                ),
                "SYNDA": (
                    "{activity}/{institute}/{dataset}/{exp}/"
                    "{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
            },
            "input_file": (
                "{short_name}_{mip}_{dataset}_{exp}_{ensemble}_{grid}*.nc"
            ),
            "output_file": (
                "{project}_{dataset}_{mip}_{exp}_{ensemble}_"
                "{short_name}_{grid}"
            ),
            "cmor_type": "CMIP6",
        },
        "obs4MIPs": {
            "cmor_strict": False,
            "input_dir": {
                "default": "Tier{tier}/{dataset}",
                "ESGF": "{project}/{dataset}/{version}",
                "RCAST": "/",
                "IPSL": (
                    "{realm}/{short_name}/{freq}/{grid}/"
                    "{institute}/{dataset}/{latest_version}"
                ),
            },
            "input_file": {
                "default": "{short_name}_*.nc",
                "ESGF": "{short_name}_*.nc",
            },
            "output_file": "{project}_{dataset}_{short_name}",
            "cmor_type": "CMIP6",
            "cmor_path": "obs4mips",
            "cmor_default_table_prefix": "obs4MIPs_",
        },
    }
    return developer_config_file_contents


def create_user_config(
    cmew_data_for_esmval_dir,
    dev_config_path,
    drs_cmip6,
    drs_obs4mips,
    max_parallel_tasks,
    output_dir,
    rootpath_cmip6,
    rootpath_obs4mips,
):
    """
    Return the contents of the user configuration file.

    Parameters
    ----------
    cmew_data_for_esmval_dir:
        The full path to the directory where data
        processed with CMEW will be stored.
    dev_config_path:
        The full path to the file where the
        developer config file for ESMValTool will be written.
    drs_cmip6:
        The DRS for CMIP6.
    drs_obs4mips:
        The DRS for obs4MIPS.
    max_parallel_tasks:
        A parallelisation option to feed to ESMValTool.
    output_dir:
        The path to the directory where ESMValTool should write its output.
    rootpath_cmip6:
        The rootpath for CMIP6.
    rootpath_obs4mips:
        The rootpath for obs4MIPS.

    Returns
    -------
    dict
        The contents of the user configuration file.
    """
    max_parallel_tasks = int(max_parallel_tasks)

    # Note that 'auxiliary_data_dir' and 'download_dir'
    # are set to empty values and cannot currently be
    # configured. However, 'download_dir' is used only when using the
    # automatic download feature via ESMValTool (which we do not intend
    # to use here).
    # 'auxiliary_data_dir' is used by some recipes to look for
    # additional datasets, so may need to be configured in the future.

    user_config_file_contents = {
        "auxiliary_data_dir": "",
        "config_developer_file": dev_config_path,
        "download_dir": "",
        "drs": {
            "CMIP6": drs_cmip6,
            "obs4MIPs": drs_obs4mips,
            "ESMVal": "BADC",
        },
        "max_parallel_tasks": max_parallel_tasks,
        "output_dir": output_dir,
        "remove_preproc_dir": False,
        "rootpath": {
            "CMIP6": rootpath_cmip6,
            "obs4MIPs": rootpath_obs4mips,
            "ESMVal": cmew_data_for_esmval_dir,
        },
    }
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


def configure_recipe(
    cmew_data_for_esmval_dir,
    dev_config_path,
    drs_cmip6,
    drs_obs4mips,
    max_parallel_tasks,
    mip_table_dir,
    output_dir,
    rootpath_cmip6,
    rootpath_obs4mips,
    user_config_path,
):
    """
    Write the required user and developer configuration files for
    ESMValTool.
    """
    logger.info("Creating developer config")
    developer_config_contents = create_developer_config(mip_table_dir)
    ensure_parent_dir(dev_config_path)
    logger.info("Writing developer config to %s", dev_config_path)
    write_yaml(dev_config_path, developer_config_contents)

    logger.info("Creating user config")
    user_config_contents = create_user_config(
        cmew_data_for_esmval_dir,
        dev_config_path,
        drs_cmip6,
        drs_obs4mips,
        max_parallel_tasks,
        output_dir,
        rootpath_cmip6,
        rootpath_obs4mips,
    )
    ensure_parent_dir(user_config_path)
    logger.info("Writing user config to %s", user_config_path)
    write_yaml(user_config_path, user_config_contents)
