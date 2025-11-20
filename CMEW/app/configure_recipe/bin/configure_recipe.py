#!/usr/bin/env python
# (C) Crown Copyright 2022-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate the required user configuration file for ESMValTool.
"""
import os

import yaml


def main():
    """
    Write the required user configuration file for ESMValTool.

    The user configuration file is written to the path defined by
    the environment variable ``USER_CONFIG_PATH``.
    """
    # Retrieve the values defined in the environment for the
    # 'configure_recipe' task.
    values = retrieve_values_from_task_env()

    # Create the contents for the user configuration file using these
    # values.
    user_config_file_contents = create_user_config_file(values)

    # Write the updated configuration values to the file defined by
    # 'USER_CONFIG_PATH'.
    user_config_path = values["USER_CONFIG_PATH"]
    write_yaml(user_config_path, user_config_file_contents)


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
        "DRS_ANA4MIPS": os.environ["DRS_ANA4MIPS"],
        "DRS_CMIP3": os.environ["DRS_CMIP3"],
        "DRS_CMIP5": os.environ["DRS_CMIP5"],
        "DRS_CMIP6": os.environ["DRS_CMIP6"],
        "DRS_CORDEX": os.environ["DRS_CORDEX"],
        "DRS_NATIVE6": os.environ["DRS_NATIVE6"],
        "DRS_OBS": os.environ["DRS_OBS"],
        "DRS_OBS4MIPS": os.environ["DRS_OBS4MIPS"],
        "DRS_OBS6": os.environ["DRS_OBS6"],
        "MAX_PARALLEL_TASKS": os.environ["MAX_PARALLEL_TASKS"],
        "OUTPUT_DIR": os.environ["OUTPUT_DIR"],
        "ROOTPATH_ANA4MIPS": os.environ["ROOTPATH_ANA4MIPS"],
        "ROOTPATH_CMIP3": os.environ["ROOTPATH_CMIP3"],
        "ROOTPATH_CMIP5": os.environ["ROOTPATH_CMIP5"],
        "ROOTPATH_CMIP6": os.environ["ROOTPATH_CMIP6"],
        "ROOTPATH_CORDEX": os.environ["ROOTPATH_CORDEX"],
        "ROOTPATH_NATIVE6": os.environ["ROOTPATH_NATIVE6"],
        "ROOTPATH_OBS": os.environ["ROOTPATH_OBS"],
        "ROOTPATH_OBS4MIPS": os.environ["ROOTPATH_OBS4MIPS"],
        "ROOTPATH_OBS6": os.environ["ROOTPATH_OBS6"],
        "ROOTPATH_RAWOBS": os.environ["ROOTPATH_RAWOBS"],
        "USER_CONFIG_PATH": os.environ["USER_CONFIG_PATH"],
    }
    return values_from_task_env


def create_user_config_file(values=None):
    """
    Return the contents of the user configuration file.

    Parameters
    ----------
    values : dictionary
        The values to use for the user configuration file.

    Returns
    -------
    : dictionary
        The contents of the user configuration file.
    """
    if values is None:
        values = {}

    if "CYLC_WORKFLOW_SHARE_DIR" in values:
        config_developer_file = os.path.join(
            values["CYLC_WORKFLOW_SHARE_DIR"],
            "etc",
            "config-developer.yml",
        )
        esmval = os.path.join(
            values["CYLC_WORKFLOW_SHARE_DIR"],
            "work",
            "GCModelDev",
        )
    else:
        config_developer_file = None
        esmval = None

    if "MAX_PARALLEL_TASKS" in values:
        max_parallel_tasks = int(values["MAX_PARALLEL_TASKS"])
    else:
        max_parallel_tasks = None

    # Note that 'auxiliary_data_dir', 'download_dir' and
    # 'extra_facets_dir' are set to empty values and cannot currently be
    # configured. However, 'download_dir' is used only when using the
    # automatic download feature via ESMValTool (which we do not intend
    # to use here) and 'extra_facets_dir' is not available in the
    # default configuration file provided by ESMValTool v2.6.0.
    # 'auxiliary_data_dir' is used by some recipes to look for
    # additional datasets, so may need to be configured in the future.
    user_config_file_contents = {
        "auxiliary_data_dir": "",
        "config_file": values.get("USER_CONFIG_PATH", None),
        "config_developer_file": config_developer_file,
        "download_dir": "",
        "drs": {
            "ana4mips": values.get("DRS_ANA4MIPS", None),
            "CMIP3": values.get("DRS_CMIP3", None),
            "CMIP5": values.get("DRS_CMIP5", None),
            "CMIP6": values.get("DRS_CMIP6", None),
            "CORDEX": values.get("DRS_CORDEX", None),
            "native6": values.get("DRS_NATIVE6", None),
            "OBS": values.get("DRS_OBS", None),
            "obs4MIPs": values.get("DRS_OBS4MIPS", None),
            "OBS6": values.get("DRS_OBS6", None),
            "ESMVal": "BADC",
        },
        "extra_facets_dir": [],
        "max_parallel_tasks": max_parallel_tasks,
        "output_dir": values.get("OUTPUT_DIR", None),
        "remove_preproc_dir": False,
        "rootpath": {
            "ana4mips": values.get("ROOTPATH_ANA4MIPS", None),
            "CMIP3": values.get("ROOTPATH_CMIP3", None),
            "CMIP5": values.get("ROOTPATH_CMIP5", None),
            "CMIP6": values.get("ROOTPATH_CMIP6", None),
            "CORDEX": values.get("ROOTPATH_CORDEX", None),
            "native6": values.get("ROOTPATH_NATIVE6", None),
            "OBS": values.get("ROOTPATH_OBS", None),
            "obs4MIPs": values.get("ROOTPATH_OBS4MIPS", None),
            "OBS6": values.get("ROOTPATH_OBS6", None),
            "RAWOBS": values.get("ROOTPATH_RAWOBS", None),
            "ESMVal": esmval,
        },
    }
    return user_config_file_contents


def write_yaml(file_path, contents):
    """
    Write the contents specified by ``contents`` to the YAML
    file specified by ``file_path``.

    Parameters
    ----------
    file_path : string
        The full path to the YAML file to write the contents to.
    contents : dictionary
        The contents to write to the YAML file.
    """
    with open(file_path, "w") as file_handle:
        yaml.dump(contents, file_handle, default_flow_style=False)


if __name__ == "__main__":
    main()
