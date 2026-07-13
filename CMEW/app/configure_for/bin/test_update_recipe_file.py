# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for update_recipe_file.py

Test data files:
/app/unittest/mock_data/original_recipe_radiation_budget.yml
    input for test_return_blank_recipe
    input for test_main
/app/unittest/kgo/blank_recipe_radiation_budget.yml
    kgo for test_return_blank_recipe
/app/unittest/mock_data/updated_recipe_radiation_budget.yml
    input for test_add_extra_datasets
/app/unittest/mock_data/cmip6_datasets.yml
    input for test_add_extra_datasets
/app/unittest/mock_data/model_runs.yml
    input for test_main
/app/unittest/kgo/extended_radiation_budget_recipe.yml
    kgo for test_add_extra_datasets
    kgo for test_main
"""
from update_recipe_file import (
    return_blank_recipe,
    add_extra_datasets,
    remove_additional_datasets,
    update_recipe_file,
)
from pathlib import Path
import shutil
import yaml


mock_data_dir = Path(__file__).parent.parent.parent / "unittest" / "mock_data"
recipe_format_file = mock_data_dir / "recipe_paths.yml"
model_runs_yml_fp = mock_data_dir / "model_runs.yml"
cmip6_datasets_yml_fp = mock_data_dir / "cmip6_datasets.yml"
original_recipe_fp = mock_data_dir / "original_recipe_radiation_budget.yml"
extra_ds_in_recipe_fp = mock_data_dir / "recipe_with_additional_datasets.yml"
updated_recipe_fp = mock_data_dir / "updated_recipe_radiation_budget.yml"

kgo_dir = Path(__file__).parent.parent.parent / "unittest" / "kgo"
no_ds_in_recipe_fp = kgo_dir / "blank_recipe_radiation_budget.yml"
no_extras_in_recipe_fp = kgo_dir / "recipe_additional_datasets_removed.yml"
extended_recipe_fp = kgo_dir / "extended_radiation_budget_recipe.yml"


def test_return_blank_recipe():
    with open(no_ds_in_recipe_fp, "r") as file_handle:
        expected = yaml.safe_load(file_handle)
    actual = return_blank_recipe(str(original_recipe_fp))
    assert actual == expected


def test_add_extra_datasets():
    with open(extended_recipe_fp, "r") as file_handle_1:
        expected = yaml.safe_load(file_handle_1)

    with open(updated_recipe_fp, "r") as file_handle_2:
        pre_recipe = yaml.safe_load(file_handle_2)

    # Using str(filepath) here as update_recipe_file.py uses os, not pathlib
    actual = add_extra_datasets(pre_recipe, str(cmip6_datasets_yml_fp))
    assert actual == expected


def test_remove_additional_datasets():
    recipe_id = "mock_entry"
    with open(no_extras_in_recipe_fp, "r") as file_handle_1:
        expected = yaml.safe_load(file_handle_1)

    with open(extra_ds_in_recipe_fp, "r") as file_handle_2:
        pre_recipe = yaml.safe_load(file_handle_2)

    # Using str(filepath) here as update_recipe_file.py uses os, not pathlib
    actual = remove_additional_datasets(
        pre_recipe, recipe_id, str(recipe_format_file)
    )
    assert actual == expected


def test_update_recipe_file(tmp_path):
    """update_recipe_file() should overwrite the recipe in place."""
    # Copy the original recipe to a tmp_path location to allow it to be
    # overwritten.
    path_to_temp_recipe = tmp_path / "tmp_recipe.yml"
    shutil.copy(original_recipe_fp, path_to_temp_recipe)

    # Mock the environmental variable 'RECIPE PATH' to the tmp_path location
    # where the original recipe is stored.
    recipe_path = str(path_to_temp_recipe)

    # These are used to check with additional datasets are removed
    recipe_id = "radiation_budget"

    update_recipe_file(
        recipe_path,
        model_runs_yml_fp,
        cmip6_datasets_yml_fp,
        recipe_id,
        recipe_format_file,
    )

    with open(path_to_temp_recipe, "r") as file_handle_1:
        actual_lines = file_handle_1.readlines()

    with open(extended_recipe_fp, "r") as file_handle_2:
        kgo_with_comment = file_handle_2.readlines()

    # Remove the five comment lines at the top of
    # 'updated_recipe_radiation_budget.yml'.
    kgo_without_comment = kgo_with_comment[5:]

    assert actual_lines == kgo_without_comment
