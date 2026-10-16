#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
from configure_recipe import amend_site_config, amend_user_config


def test_amend_site_config():
    mock_site_local_data_key = "mock_local_key"
    mock_site_config_defaults = {
        "projects": {
            "CMIP6": {
                "data": {
                    "mock_local_key": {
                        "type": "type.to.copy",
                        "rootpath": "/path/to/data/to/be/copied",
                        "dirname_template": (
                            "{project}/{activity}/{and}/{other}/{fields}"
                        ),
                        "filename_template": (
                            "{template}_{to}_{be}_{copied}*.nc"
                        ),
                    }
                }
            },
            "Other_data": {
                "data": {
                    "mock_local_key": {
                        "type": "other.type.of.data",
                        "rootpath": "/path/to/different/data",
                        "dirname_template": "{some}/{different}/{fields}",
                        "filename_template": "{a}_{b}_{c}*.nc",
                    }
                }
            },
        }
    }
    mock_cmew_data_for_esmval_dir = "/path/to/CMEW/data"
    expected = {
        "projects": {
            "CMIP6": {
                "data": {
                    "mock_local_key": {
                        "type": "type.to.copy",
                        "rootpath": "/path/to/data/to/be/copied",
                        "dirname_template": (
                            "{project}/{activity}/{and}/{other}/{fields}"
                        ),
                        "filename_template": (
                            "{template}_{to}_{be}_{copied}*.nc"
                        ),
                    }
                }
            },
            "Other_data": {
                "data": {
                    "mock_local_key": {
                        "type": "other.type.of.data",
                        "rootpath": "/path/to/different/data",
                        "dirname_template": "{some}/{different}/{fields}",
                        "filename_template": "{a}_{b}_{c}*.nc",
                    }
                }
            },
            "ESMVal": {
                "data": {
                    "local": {
                        "type": "type.to.copy",
                        "filename_template": (
                            "{template}_{to}_{be}_{copied}*.nc"
                        ),
                        "rootpath": "/path/to/CMEW/data",
                        "dirname_template": (
                            "{project}/{institute}/{dataset}/{exp}"
                            "/{ensemble}/{mip}/{short_name}/{grid}/{version}"
                        ),
                    }
                }
            },
        }
    }
    actual = amend_site_config(
        mock_site_config_defaults,
        mock_site_local_data_key,
        mock_cmew_data_for_esmval_dir,
    )
    assert actual == expected


def test_amend_user_config():
    mock_user_config_defaults = {
        "other_field": "a string",
        "output_dir": "/default/output/dir/to/overwrite",
        "max_parallel_tasks": "null",
    }
    mock_max_parallel_tasks = "99"
    mock_output_dir = "/given/output/dir"
    actual = amend_user_config(
        mock_user_config_defaults,
        mock_max_parallel_tasks,
        mock_output_dir,
    )
    expected = {
        "other_field": "a string",
        "output_dir": "/given/output/dir",
        "max_parallel_tasks": 99,
        "remove_preproc_dir": False,
    }
    assert actual == expected
