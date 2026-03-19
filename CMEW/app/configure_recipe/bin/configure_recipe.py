#!/usr/bin/env python
# (C) Crown Copyright 2022-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate the required user configuration file for ESMValTool.
"""

import os
import yaml


def main():
    """
    Write the required user and developer configuration files for
    ESMValTool.
    """
    values = retrieve_values_from_task_env()
    developer_config_path = values["DEV_CONFIG_PATH"]
    developer_config_contents = create_developer_config(values)
    ensure_parent_dir(developer_config_path)
    write_yaml(developer_config_path, developer_config_contents)

    values["CONFIG_DEVELOPER_FILE"] = developer_config_path

    user_config_path = values["USER_CONFIG_PATH"]
    user_config_contents = create_user_config(values)
    ensure_parent_dir(user_config_path)
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
        "MIP_TABLE_DIR": os.environ["MIP_TABLE_DIR"],
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


def create_developer_config(values):
    """
    Return the contents of the developer configuration file.

    Parameters
    ----------
    values : dict
        Configuration values.

    Returns
    -------
    dict
        Developer configuration content.
    """
    mip_table_dir = values["MIP_TABLE_DIR"]

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
        "CMIP5": {
            "cmor_strict": True,
            "input_dir": {
                "default": "/",
                "BADC": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{mip}/{ensemble}/{version}/"
                    "{short_name}"
                ),
                "BSC": "{type}/{project}/{exp}/{dataset.lower}",
                "CP4CDS": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{mip}/{ensemble}/{short_name}/"
                    "latest/"
                ),
                "DKRZ": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{mip}/{ensemble}/{version}/"
                    "{short_name}"
                ),
                "ETHZ": "{exp}/{mip}/{short_name}/{dataset}/{ensemble}/",
                "ESGF": (
                    "{project.lower}/{product}/{institute}/{dataset}/"
                    "{exp}/{frequency}/{modeling_realm}/{mip}/"
                    "{ensemble}/{version}"
                ),
                "RCAST": "{exp}/{mip}/{short_name}/{dataset}/{ensemble}/",
                "SMHI": "{dataset}/{ensemble}/{exp}/{frequency}",
                "SYNDA": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{mip}/{ensemble}/{version}"
                ),
            },
            "input_file": "{short_name}_{mip}_{dataset}_{exp}_{ensemble}*.nc",
            "output_file": (
                "{project}_{dataset}_{mip}_{exp}_{ensemble}_{short_name}"
            ),
        },
        "CMIP3": {
            "cmor_strict": True,
            "input_dir": {
                "default": "/",
                "BADC": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{short_name}/{ensemble}/{version}"
                ),
                "DKRZ": (
                    "{exp}/{modeling_realm}/{frequency}/{short_name}/"
                    "{dataset}/{ensemble}"
                ),
                "ESGF": (
                    "{project.lower}/{institute}/{dataset}/{exp}/"
                    "{frequency}/{modeling_realm}/{ensemble}/"
                    "{short_name}/{version}"
                ),
                "IPSL": (
                    "{institute}/{dataset}/{exp}/{frequency}/"
                    "{modeling_realm}/{ensemble}/{short_name}/"
                    "{version}/{short_name}"
                ),
            },
            "input_file": "{short_name}_*.nc",
            "output_file": (
                "{project}_{institute}_{dataset}_{mip}_{exp}_"
                "{ensemble}_{short_name}"
            ),
            "cmor_type": "CMIP3",
        },
        "OBS": {
            "cmor_strict": False,
            "input_dir": {
                "default": "Tier{tier}/{dataset}",
                "BSC": (
                    "{type}/{institute.lower}/{dataset.lower}/"
                    "{freq_folder}/{short_name}{freq_base}"
                ),
                "RCAST": "{dataset}",
            },
            "input_file": {
                "default": (
                    "{project}_{dataset}_{type}_{version}_{mip}_"
                    "{short_name}[_.]*nc"
                ),
                "BSC": "{short_name}_*.nc",
                "RCAST": "{short_name}_{mip}_{type}_{dataset}_*.nc",
            },
            "output_file": (
                "{project}_{dataset}_{type}_{version}_{mip}_{short_name}"
            ),
            "cmor_type": "CMIP5",
        },
        "OBS6": {
            "cmor_strict": False,
            "input_dir": {
                "default": "Tier{tier}/{dataset}",
                "BSC": (
                    "{type}/{institute.lower}/{dataset.lower}/"
                    "{freq_folder}/{short_name}{freq_base}"
                ),
            },
            "input_file": {
                "default": (
                    "{project}_{dataset}_{type}_{version}_{mip}_"
                    "{short_name}[_.]*nc"
                ),
                "BSC": "{short_name}_*.nc",
            },
            "output_file": (
                "{project}_{dataset}_{type}_{version}_{mip}_{short_name}"
            ),
            "cmor_type": "CMIP6",
        },
        "native6": {
            "cmor_strict": False,
            "input_dir": {
                "default": (
                    "Tier{tier}/{dataset}/{version}/{frequency}/"
                    "{short_name}"
                ),
            },
            "input_file": {
                "default": "*.nc",
            },
            "output_file": (
                "{project}_{dataset}_{type}_{version}_{mip}_{short_name}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "CMIP6_",
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
        "ana4mips": {
            "cmor_strict": False,
            "input_dir": {
                "default": "Tier{tier}/{dataset}",
                "RCAST": "/",
            },
            "input_file": "{short_name}_{mip}_{type}_{dataset}_*.nc",
            "output_file": "{project}_{mip}_{type}_{dataset}_{short_name}",
            "cmor_type": "CMIP5",
        },
        "EMAC": {
            "cmor_strict": False,
            "input_dir": {
                "default": "{exp}/{channel}",
            },
            "input_file": {
                "default": "{exp}*{channel}{postproc_flag}.nc",
            },
            "output_file": (
                "{project}_{dataset}_{exp}_{channel}_{mip}_{short_name}"
            ),
            "cmor_type": "CMIP6",
            "ignore_warnings": {
                "load": [
                    {
                        "message": (
                            "Ignored formula of unrecognised type: .*"
                        ),
                        "module": "iris",
                    },
                    {
                        "message": (
                            "Ignoring formula terms variable .* "
                            "referenced by data variable .* via "
                            "variable .*"
                        ),
                        "module": "iris",
                    },
                    {
                        "message": (
                            "Missing CF-netCDF formula term variable "
                            ".*, referenced by netCDF variable .*"
                        ),
                        "module": "iris",
                    },
                    {
                        "message": (
                            "NetCDF variable .* contains unknown cell "
                            "method .*"
                        ),
                        "module": "iris",
                    },
                ],
            },
        },
        "CORDEX": {
            "input_dir": {
                "default": "/",
                "spec": (
                    "{domain}/{institute}/{driver}/{exp}/{ensemble}/"
                    "{dataset}/{rcm_version}/{mip}/{short_name}"
                ),
                "BADC": (
                    "{domain}/{institute}/{driver}/{exp}/{ensemble}/"
                    "{dataset}/{rcm_version}/{mip}/{short_name}/"
                    "{version}"
                ),
                "ESGF": (
                    "{project.lower}/output/{domain}/{institute}/"
                    "{driver}/{exp}/{ensemble}/{dataset}/"
                    "{rcm_version}/{frequency}/{short_name}/{version}"
                ),
            },
            "input_file": (
                "{short_name}_{domain}_{driver}_{exp}_{ensemble}_"
                "{dataset}_{rcm_version}_{mip}*.nc"
            ),
            "output_file": (
                "{project}_{dataset}_{rcm_version}_{driver}_{domain}_"
                "{mip}_{exp}_{ensemble}_{short_name}"
            ),
            "cmor_type": "CMIP5",
            "cmor_path": "cordex",
        },
        "IPSLCM": {
            "cmor_strict": False,
            "input_dir": {
                "default": (
                    "{root}/{account}/{model}/{status}/{exp}/"
                    "{simulation}/{dir}/{out}/{freq}"
                ),
            },
            "input_file": {
                "default": [
                    "{simulation}_*_{ipsl_varname}.nc",
                    "{simulation}_*_{group}.nc",
                ],
            },
            "output_file": (
                "{dataset}_{account}_{model}_{status}_{exp}_"
                "{simulation}_{freq}_{short_name}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "CMIP6_",
        },
        "ICON": {
            "cmor_strict": False,
            "input_dir": {
                "default": [
                    "{exp}",
                    "{exp}/outdata",
                ],
            },
            "input_file": {
                "default": "{exp}_{var_type}*.nc",
            },
            "output_file": (
                "{project}_{dataset}_{exp}_{var_type}_{mip}_{short_name}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "CMIP6_",
        },
        "CESM": {
            "cmor_strict": False,
            "input_dir": {
                "default": [
                    "/",
                    "{case}/{gcomp}/hist",
                    "{case}/{gcomp}/proc/{tdir}/{tperiod}",
                ],
            },
            "input_file": {
                "default": "{case}.{scomp}.{type}.{string}*nc",
            },
            "output_file": (
                "{project}_{dataset}_{case}_{gcomp}_{scomp}_{type}_"
                "{mip}_{short_name}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "CMIP6_",
        },
    }
    return developer_config_file_contents


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
        "config_developer_file": values.get("CONFIG_DEVELOPER_FILE"),
        "download_dir": "",
        "drs": {
            "ana4mips": values.get("DRS_ANA4MIPS"),
            "CMIP3": values.get("DRS_CMIP3"),
            "CMIP5": values.get("DRS_CMIP5"),
            "CMIP6": values.get("DRS_CMIP6"),
            "CORDEX": values.get("DRS_CORDEX"),
            "native6": values.get("DRS_NATIVE6"),
            "OBS": values.get("DRS_OBS"),
            "obs4MIPs": values.get("DRS_OBS4MIPS"),
            "OBS6": values.get("DRS_OBS6"),
            "ESMVal": "BADC",
        },
        "extra_facets_dir": [],
        "max_parallel_tasks": max_parallel_tasks,
        "output_dir": values.get("OUTPUT_DIR"),
        "remove_preproc_dir": False,
        "rootpath": {
            "ana4mips": values.get("ROOTPATH_ANA4MIPS"),
            "CMIP3": values.get("ROOTPATH_CMIP3"),
            "CMIP5": values.get("ROOTPATH_CMIP5"),
            "CMIP6": values.get("ROOTPATH_CMIP6"),
            "CORDEX": values.get("ROOTPATH_CORDEX"),
            "native6": values.get("ROOTPATH_NATIVE6"),
            "OBS": values.get("ROOTPATH_OBS"),
            "obs4MIPs": values.get("ROOTPATH_OBS4MIPS"),
            "OBS6": values.get("ROOTPATH_OBS6"),
            "RAWOBS": values.get("ROOTPATH_RAWOBS"),
            "ESMVal": esmval,
        },
    }
    return user_config_file_contents


def ensure_parent_dir(file_path):
    """
    Create the parent directory for ``file_path`` if needed.
    """
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
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
