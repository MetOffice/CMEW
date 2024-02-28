#!/usr/bin/env python
# (C) Crown Copyright 2024, Met Office.
# Please see LICENSE.md for license details.
import pytest
from configure_process import create_user_config_file

config_file = create_user_config_file()


@pytest.mark.parametrize(
    "actual,expected",
    [
        (config_file["remove_preproc_dir"], False),
        (config_file["drs"]["ESMVal"], "BADC"),
    ],
)
def test_user_config_file_contents(actual, expected):
    assert actual == expected
