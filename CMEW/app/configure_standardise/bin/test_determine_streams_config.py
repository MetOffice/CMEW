# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for determine_streams_config.py

Test data files:
/app/unittest/mock_data/model_run_stream_test.yml
    input for test_create_request
"""
import pytest
from pathlib import Path
from determine_streams_config import determine_stream_config_fp


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv(
        "MODEL_RUNS_CONFIG",
        str(
            Path(__file__).parent.parent.parent
            / "unittest"
            / "mock_data"
            / "model_run_stream_config.yml"
        )
    )
    monkeypatch.setenv("DEFAULT_STREAM_CONFIG_PATH", "/path/to/default_streams.yml")


def test_determine_stream_config_fp_custom(mock_env_vars, monkeypatch):
    monkeypatch.setenv("CYLC_TASK_PARAM_dataset", "run-1")
    expected = "/path/to/custom_streams.yml"
    actual = determine_stream_config_fp()
    assert actual == expected

def test_determine_stream_config_fp_default(mock_env_vars, monkeypatch):
    monkeypatch.setenv("CYLC_TASK_PARAM_dataset", "run-2")
    expected = "/path/to/default_streams.yml"
    actual = determine_stream_config_fp()
    assert actual == expected
