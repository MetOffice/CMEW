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


mock_recipe_dict = {
    "mock_entry": {
        "recipe_name": "recipe_specified_name.yml",
        "recipe_fp": "subdir_1/recipe_second_name.yml",
        "empty_additional_datasets": True,
    },
}


def test_retrieve_specified(monkeypatch):
    monkeypatch.setenv("CYLC_TASK_PARAM_recipe", "mock_entry")
    expected = "recipe_specified_name.yml", "subdir_1/recipe_second_name.yml"
    actual = retrieve_name_and_fp(mock_recipe_dict)

    assert actual == expected


def test_retrieve_defaults(monkeypatch):
    monkeypatch.setenv("CYLC_TASK_PARAM_recipe", "not_here")
    expected = "recipe_not_here.yml", "recipe_not_here.yml"
    actual = retrieve_name_and_fp(mock_recipe_dict)

    assert actual == expected
