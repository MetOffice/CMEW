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


mock_data_dir = Path(__file__).parent.parent.parent / "unittest" / "mock_data"
recipe_format_file = mock_data_dir / "recipe_paths.yml"


def test_retrieve_specified():
    test_recipe_id = "mock_entry"
    expected = "recipe_specified_name.yml", "subdir_1/recipe_second_name.yml"
    actual = retrieve_name_and_fp(test_recipe_id, str(recipe_format_file))

    assert actual == expected


def test_retrieve_defaults():
    test_recipe_id = "not_here"
    expected = "recipe_not_here.yml", "recipe_not_here.yml"
    actual = retrieve_name_and_fp(test_recipe_id, str(recipe_format_file))

    assert actual == expected
