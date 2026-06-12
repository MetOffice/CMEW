#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
import pytest
from pathlib import Path
import yaml
from configure_recipe import retrieve_values_from_task_env, retrieve_default_settings, create_user_config

# For inputs and expected outputs
expected_values = {
    "CYLC_WORKFLOW_SHARE_DIR": "/fake/workflow/share",
    "MAX_PARALLEL_TASKS": "99",
    "OUTPUT_DIR": "/fake/output/dir",
    "ROOTPATH_CMIP6": "/fake/cmip6/data",
    "ROOTPATH_OBS": "/fake/obs/data",
    "ROOTPATH_OBS4MIPS": "/fake/obs4mips/data",
    "USER_CONFIG_PATH": "/path/to/write/config/to",
}

 # For input and outputs
path_to_mock_defaults= str(
    Path(__file__).parent.parent.parent
    / "unittest"
    / "mock_data"
    / "esmval_defaults.yml"
)

 # For checking outputs
path_to_kgo_config = str(
    Path(__file__).parent.parent.parent
    / "unittest"
    / "kgo"
    / "esmval_defaults.yml"
)


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("CYLC_WORKFLOW_SHARE_DIR", "/fake/workflow/share")
    monkeypatch.setenv("MAX_PARALLEL_TASKS", "99")
    monkeypatch.setenv("OUTPUT_DIR", "/fake/output/dir")
    monkeypatch.setenv("ROOTPATH_CMIP6", "/fake/cmip6/data")
    monkeypatch.setenv("ROOTPATH_OBS", "/fake/obs/data")
    monkeypatch.setenv("ROOTPATH_OBS4MIPS", "/fake/obs4mips/data")
    monkeypatch.setenv("USER_CONFIG_PATH", "/path/to/write/config/to")
    monkeypatch.setenv("ESMVAL_CONFIG_DEFAULT_PATH", path_to_mock_defaults)


def test_retrieve_values_from_task_env(mock_env_vars):
    expected = expected_values
    actual = retrieve_values_from_task_env()
    assert expected == actual


# I'm unconvinced that this can / should be tested in this way
# as I want it as input for the next one testing at all seems better than not
def test_retrieve_default_settings(mock_env_vars):
    with open(path_to_mock_defaults, "r") as f:
        expected = yaml.safe_load(f)
    actual = retrieve_default_settings()
    assert expected == actual


def test_create_user_config(mock_env_vars):
    with open(path_to_kgo_config, "r") as f:
        expected = yaml.safe_load(f)
    actual = create_user_config(retrieve_default_settings(), expected_values)
    assert expected == actual
