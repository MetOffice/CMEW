#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
from configure_process import create_user_config_file


def test_create_user_config_file():
    config_values = create_user_config_file()
    print(config_values)
    output = config_values["remove_preproc_dir"]
    expected = False
    assert output == expected
