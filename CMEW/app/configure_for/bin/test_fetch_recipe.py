#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for fetch_recipe.py

Test data files:
/app/unittest/mock_data/recipe_paths.yml
    input for test_retrieve_specified, test_retrieve_defaults
"""
from fetch_recipe import retrieve_name_and_fp
from pathlib import Path
import pytest


@pytest.fixture
def mock_env_vars(monkeypatch):
    # For adding extra datasets
    monkeypatch.setenv(
        "RECIPE_DICT_PATH",
        str(
            Path(__file__).parent.parent.parent
            / "unittest"
            / "mock_data"
            / "recipe_paths.yml"
        ),
    )


def test_retrieve_specified(mock_env_vars):
    key = "mock_entry"
    expected = "recipe_specified_name.yml", "subdir_1/recipe_second_name.yml"
    actual = retrieve_name_and_fp(key)

    assert actual == expected


def test_retrieve_defaults(mock_env_vars):
    key = "not_here"
    expected = "recipe_not_here.yml", "recipe_not_here.yml"
    actual = retrieve_name_and_fp(key)

    assert actual == expected
