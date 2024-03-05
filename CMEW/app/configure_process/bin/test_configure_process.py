#!/usr/bin/env python
# (C) Crown Copyright 2024, Met Office.
# Please see LICENSE.md for license details.
import pytest
from configure_process import create_user_config_file


def test_create_user_config_file_verify_remove_preproc_dir_value_is_false():
    config_values = create_user_config_file()

    output = config_values["remove_preproc_dir"]
    expected = False
    assert output == expected


def test_create_user_config_file_verify_esmval_value_equals_BADC():
    config_values = create_user_config_file()

    output = config_values["drs"]["ESMVal"]
    expected = "BADC"
    assert output == expected


def test_create_user_config_file_verify_user_config_path():
    expected = "userpath"
    test_values = {"USER_CONFIG_PATH": expected}
    config_values = create_user_config_file(test_values)

    output = config_values["config_file"]
    assert output == expected


def test_create_user_config_file_verify_cmip6_rootpath():
    expected = "cmip_rootpath"
    test_values = {"ROOTPATH_CMIP6": expected}
    config_values = create_user_config_file(test_values)

    output = config_values["rootpath"]["CMIP6"]
    assert output == expected


@pytest.mark.parametrize(
    "input_key, output_outer_key, output_inner_key, expected",
    [
        ("DRS_CORDEX", "drs", "CORDEX", "cordexpath"),
        ("DRS_OBS", "drs", "OBS", "obspath"),
    ],
)
def test_create_user_config_file_two_values(
    input_key, output_outer_key, output_inner_key, expected
):
    test_values = {input_key: expected}
    config_values = create_user_config_file(test_values)
    output = config_values[output_outer_key][output_inner_key]
    assert output == expected
