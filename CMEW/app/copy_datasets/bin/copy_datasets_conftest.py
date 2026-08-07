#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def model_runs_nl_fp():
    return mock_data_dir() / "model_runs.nl"


def model_runs_as_list_yml_fp():
    return mock_data_dir() / "model_runs_as_list.yml"


def kgo_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "kgo"


def basic_dict_yml_fp():
    return kgo_dir() / "basic_dict.yml"


def model_runs_as_dict_yml_fp():
    return kgo_dir() / "model_runs_as_dict.yml"
