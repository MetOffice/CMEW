#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def kgo_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "kgo"


def variables_txt_fp():
    return kgo_dir() / "variables.txt"


def etc_dir():
    return Path(__file__).parent.parent / "etc"


def streams_yml_fp():
    return etc_dir() / "streams.yml"
