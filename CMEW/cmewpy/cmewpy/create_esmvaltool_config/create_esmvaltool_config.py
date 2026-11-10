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
from copy import deepcopy

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


def amend_site_config(
    site_config_defaults,
    site_local_data_key,
    cmew_data_for_esmval_dir,
):
    """
    Return the updated site site-specific configuration for ESMValTool.

    A new section titled "ESMVal" is added
    and is a copy of the facets from the CMIP6 entry.

    Parameters
    ----------
    site_config_defaults:
        The contents of the
        default site-specific configuration for ESMValTool.
    site_local_data_key : str
        The site-specific identifier in the ESMValCore configuration file
        `data-hpc-<site_local_data_key>.yml`
        in `ESMValCore/esmvalcore/config/configurations`
        and also used as a key in the dictionary
        [projects][<project>][data][<site_local_data_key>]
        in said configuration file.
    cmew_data_for_esmval_dir : str
        The full path to the parent directory where data processed with CDDS
        will be stored for passing to ESMValTool.

    Returns
    -------
    dict
        The updated site-specific configuration for ESMValTool.
    """
    site_config_file_contents = site_config_defaults

    # There is an assumption that the string from
    # {"badc","bsc","dkrz-era5-grib","dkrz","ipsl","mo","nci"},
    # i.e. the string used in the `data-hpc-<key>.yml` filename,
    # will be the fourth-level key here,
    # and that the type and filename templates are the same as for CMIP6 data.

    # Add a section for finding CMEW data
    site_config_file_contents["projects"]["ESMVal"] = deepcopy(
        site_config_file_contents["projects"]["CMIP6"]
    )

    # But CMEW data is stored locally to the CMEW workflow
    site_config_file_contents["projects"]["ESMVal"]["data"][
        site_local_data_key
    ]["rootpath"] = cmew_data_for_esmval_dir

    # And the directory structure template misses the 'activity' level
    site_config_file_contents["projects"]["ESMVal"]["data"][
        site_local_data_key
    ]["dirname_template"] = (
        "{project}/{institute}/{dataset}/{exp}/"
        "{ensemble}/{mip}/{short_name}/{grid}/{version}"
    )

    logger.debug("Site config file contents:\n%s", site_config_file_contents)
    return site_config_file_contents


def amend_user_config(
    user_config_defaults,
    max_parallel_tasks,
    output_dir,
):
    """
    Return the updated user-specific configuration for ESMValTool.

    Parameters
    ----------
    user_config_defaults : dict
        The contents of the
        user-specific configuration for ESMValTool.
    max_parallel_tasks : str
        A parallelisation option to feed to ESMValTool.
    output_dir : str
        The path to the directory where ESMValTool should write its output.

    Returns
    -------
    dict
        The contents of the user configuration file.
    """
    max_parallel_tasks = int(max_parallel_tasks)

    # Overwrite with changes from default config
    user_config_file_contents = user_config_defaults
    user_config_defaults["max_parallel_tasks"] = max_parallel_tasks
    user_config_defaults["output_dir"] = output_dir
    user_config_defaults["remove_preproc_dir"] = False

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


def create_esmvaltool_config(
    site_config_defaults_filepath,
    user_config_defaults_filepath,
    site_local_data_key,
    cmew_data_for_esmval_dir,
    max_parallel_tasks,
    output_dir,
    site_config_output_path,
    user_config_output_path,
):
    """
    Write the required configuration files for ESMValTool.

    Parameters
    ----------
    site_config_defaults_filepath : str
        The full path to the YAML file containing the
        default site-specific configuration for ESMValTool.
    user_config_defaults_filepath : str
        The full path to the YAML file containing the
        default user-specific configuration for ESMValTool.
    site_local_data_key : str
        The site-specific identifier in the ESMValCore configuration file
        `data-hpc-<site_local_data_key>.yml`
        in `ESMValCore/esmvalcore/config/configurations`
        and also used as a key in the dictionary
        [projects][<project>][data][<site_local_data_key>]
        in said configuration file.
    cmew_data_for_esmval_dir : str
        The full path to the parent directory where data processed with CDDS
        will be stored for passing to ESMValTool.
    max_parallel_tasks : str
        A parallelisation option to feed to ESMValTool.
    output_dir : str
        The full path to the directory for ESMValTool to write its output.
    site_config_output_path : str
        The full path to the YAML file where the
        site-specific configuration for ESMValTool will be written.
    user_config_output_path : str
        The full path to the YAML file where the
        user-specific configuration for ESMValTool will be written.
    """
    logger.info("Creating ESMValTool site config")
    site_config_defaults = load_yaml(site_config_defaults_filepath)
    site_config_contents = amend_site_config(
        site_config_defaults, site_local_data_key, cmew_data_for_esmval_dir
    )
    ensure_parent_dir(site_config_output_path)
    logger.info("Writing site config to %s", site_config_output_path)
    write_yaml(site_config_output_path, site_config_contents)

    logger.info("Creating ESMValTool user config")
    user_config_defaults = load_yaml(user_config_defaults_filepath)
    user_config_contents = amend_user_config(
        user_config_defaults,
        max_parallel_tasks,
        output_dir,
    )
    ensure_parent_dir(user_config_output_path)
    logger.info("Writing user config to %s", user_config_output_path)
    write_yaml(user_config_output_path, user_config_contents)
