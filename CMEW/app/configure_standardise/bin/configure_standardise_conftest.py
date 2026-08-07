#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def model_runs_yml_fp():
    return mock_data_dir() / "model_runs.yml"


def kgo_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "kgo"


def request_u_cw673_cfg_fp():
    return kgo_dir() / "request_u-cw673.cfg"


def etc_dir():
    return Path(__file__).parent.parent / "etc"


def request_defaults_yml_fp():
    return etc_dir() / "request_defaults.yml"
