#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
import pytest
from configure_recipe import create_user_config, create_developer_config


@pytest.mark.parametrize(
    "input_key, output_key, expected",
    [
        (None, "remove_preproc_dir", False),
    ],
)
def test_create_user_config_file_single_values(
    input_key, output_key, expected
):
    if input_key is None:
        test_values = None
    else:
        test_values = {input_key: expected}

    config_values = create_user_config(test_values)
    actual = config_values[output_key]
    assert actual == expected


@pytest.mark.parametrize(
    "input_key, output_outer_key, output_inner_key, expected",
    [
        ("DRS_CORDEX", "drs", "CORDEX", "cordexpath"),
        ("DRS_OBS", "drs", "OBS", "obspath"),
        ("ROOTPATH_CMIP6", "rootpath", "CMIP6", "cmip_rootpath"),
        ("ESMVal", "drs", "ESMVal", "BADC"),
    ],
)
def test_create_user_config_file_nested_values(
    input_key, output_outer_key, output_inner_key, expected
):
    if input_key is None:
        test_values = None
    else:
        test_values = {input_key: expected}

    config_values = create_user_config(test_values)
    actual = config_values[output_outer_key][output_inner_key]
    assert actual == expected


@pytest.mark.parametrize(
    "input_key, output_outer_key, output_inner_key, expected",
    [
        ("MIP_TABLE_DIR", "custom", "cmor_path", "test_mip_tables"),
        ("ESMVal", "ESMVal", "cmor_type", "CMIP6"),
        ("CMIP6", "CMIP6", "cmor_type", "CMIP6"),
        ("CMIP3", "CMIP3", "cmor_type", "CMIP3"),
        ("OBS", "OBS", "cmor_type", "CMIP5"),
        ("obs4MIPs", "obs4MIPs", "cmor_path", "obs4mips"),
        ("CORDEX", "CORDEX", "cmor_path", "cordex"),
    ],
)
def test_create_developer_config_nested_values(
    input_key, output_outer_key, output_inner_key, expected
):
    if input_key == "MIP_TABLE_DIR":
        test_values = {input_key: expected}
    else:
        test_values = {"MIP_TABLE_DIR": "test_mip_tables"}

    config_values = create_developer_config(test_values)
    actual = config_values[output_outer_key][output_inner_key]
    assert actual == expected


@pytest.mark.parametrize(
    "output_outer_key, output_inner_key, expected",
    [
        ("ESMVal", "cmor_strict", True),
        ("CMIP5", "cmor_strict", True),
        ("OBS", "cmor_strict", False),
        ("native6", "cmor_default_table_prefix", "CMIP6_"),
        ("ESMVal", "cmor_default_table_prefix", "GCModelDev_"),
        ("obs4MIPs", "cmor_default_table_prefix", "obs4MIPs_"),
    ],
)
def test_create_developer_config_fixed_values(
    output_outer_key, output_inner_key, expected
):
    test_values = {"MIP_TABLE_DIR": "test_mip_tables"}

    config_values = create_developer_config(test_values)
    actual = config_values[output_outer_key][output_inner_key]
    assert actual == expected
