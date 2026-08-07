#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
from configure_recipe import create_user_config, create_developer_config


def test_create_user_config():
    test_cmew_data_for_esmval_dir = "test/cmew/esmval/dir"
    test_dev_config_path = "/test/dev/config.yml"
    test_drs_cmip6 = "test_cmip6_drs"
    test_drs_obs4mips = "test_obs4mips_drs"
    test_max_parallel_tasks = "99"
    test_output_dir = "/test/output/dir"
    test_rootpath_cmip6 = "test_cmip6_rootpath"
    test_rootpath_obs4mips = "test_obs4mips_rootpath"

    expected = {
        "auxiliary_data_dir": "",
        "config_developer_file": test_dev_config_path,
        "download_dir": "",
        "drs": {
            "CMIP6": test_drs_cmip6,
            "obs4MIPs": test_drs_obs4mips,
            "ESMVal": "BADC",
        },
        "max_parallel_tasks": int(test_max_parallel_tasks),
        "output_dir": test_output_dir,
        "remove_preproc_dir": False,
        "rootpath": {
            "CMIP6": test_rootpath_cmip6,
            "obs4MIPs": test_rootpath_obs4mips,
            "ESMVal": test_cmew_data_for_esmval_dir,
        },
    }

    actual = create_user_config(
        test_cmew_data_for_esmval_dir,
        test_dev_config_path,
        test_drs_cmip6,
        test_drs_obs4mips,
        test_max_parallel_tasks,
        test_output_dir,
        test_rootpath_cmip6,
        test_rootpath_obs4mips,
    )

    assert actual == expected


def test_create_developer_config():
    test_mip_table_dir = "/test/mip/table/dir"

    expected = {
        "custom": {
            "cmor_path": test_mip_table_dir,
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
                "{short_name}_{mip}_{dataset}_{exp}_{ensemble}" "_{grid}*.nc"
            ),
            "output_file": (
                "{project}_{dataset}_{mip}_{exp}_{ensemble}"
                "_{short_name}_{grid}"
            ),
            "cmor_type": "CMIP6",
            "cmor_default_table_prefix": "GCModelDev_",
        },
        "CMIP6": {
            "cmor_strict": True,
            "input_dir": {
                "default": "/",
                "BADC": (
                    "{activity}/{institute}/{dataset}/{exp}/{ensemble}"
                    "/{mip}/{short_name}/{grid}/{version}"
                ),
                "DKRZ": (
                    "{activity}/{institute}/{dataset}/{exp}/{ensemble}"
                    "/{mip}/{short_name}/{grid}/{version}"
                ),
                "ESGF": (
                    "{project}/{activity}/{institute}/{dataset}/{exp}"
                    "/{ensemble}/{mip}/{short_name}/{grid}/{version}"
                ),
                "ETHZ": (
                    "{exp}/{mip}/{short_name}/{dataset}/{ensemble}" "/{grid}/"
                ),
                "SYNDA": (
                    "{activity}/{institute}/{dataset}/{exp}/{ensemble}"
                    "/{mip}/{short_name}/{grid}/{version}"
                ),
            },
            "input_file": (
                "{short_name}_{mip}_{dataset}_{exp}_{ensemble}" "_{grid}*.nc"
            ),
            "output_file": (
                "{project}_{dataset}_{mip}_{exp}_{ensemble}"
                "_{short_name}_{grid}"
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
                    "{realm}/{short_name}/{freq}/{grid}/{institute}"
                    "/{dataset}/{latest_version}"
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

    actual = create_developer_config(test_mip_table_dir)

    assert actual == expected
