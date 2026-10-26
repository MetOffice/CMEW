# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for 'update_recipe_file.py'.
"""
from cmewpy.configure_for.update_recipe_file import (
    remove_datasets_contents,
    remove_additional_datasets,
    construct_datasets_contents,
    add_datasets_contents,
)


def test_remove_datasets_contents(
    recipe_with_datasets, recipe_without_datasets
):
    actual = remove_datasets_contents(recipe_with_datasets)
    expected = recipe_without_datasets
    assert actual == expected


def test_remove_additional_datasets(
    recipe_with_datasets, recipe_without_additional_datasets
):
    actual = remove_additional_datasets(recipe_with_datasets)
    expected = recipe_without_additional_datasets
    assert actual == expected


def test_construct_datasets_contents(model_datasets, cmip6_datasets, datasets):
    actual = construct_datasets_contents([model_datasets, cmip6_datasets])
    expected = datasets
    assert actual == expected


def test_add_datasets_contents(
    recipe_without_datasets, datasets, recipe_with_datasets
):
    actual = add_datasets_contents(recipe_without_datasets, datasets)
    expected = recipe_with_datasets
    assert actual == expected
