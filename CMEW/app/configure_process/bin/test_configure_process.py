#!/usr/bin/env python
# (C) Crown Copyright 2024, Met Office.
# Please see LICENSE.md for license details.
import pytest
from configure_process import create_user_config_file


@pytest.mark.parametrize(
    "input_key, output_key, expected",
    [
        ("remove_preproc_dir", "remove_preproc_dir", False),
        ("USER_CONFIG_PATH", "config_file", "userpath"),
    ],
)
def test_create_user_config_file_two_values(input_key, output_key, expected):
    test_values = {input_key: expected}
    config_values = create_user_config_file(test_values)
    output = config_values[output_key]
    assert output == expected


@pytest.mark.parametrize(
    "input_key, output_outer_key, output_inner_key, expected",
    [
        ("DRS_CORDEX", "drs", "CORDEX", "cordexpath"),
        ("DRS_OBS", "drs", "OBS", "obspath"),
        ("ROOTPATH_CMIP6", "rootpath", "CMIP6", "cmip_rootpath"),
        ("ESMVal", "drs", "ESMVal", "BADC"),
    ],
)
def test_create_user_config_file_four_values(
    input_key, output_outer_key, output_inner_key, expected
):
    test_values = {input_key: expected}
    config_values = create_user_config_file(test_values)
    output = config_values[output_outer_key][output_inner_key]
    assert output == expected
