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
from update_recipe_file import return_blank_recipe, add_extra_datasets, main
from pathlib import Path
import pytest
import shutil
import yaml


@pytest.fixture
def mock_env_vars(monkeypatch):
    # For adding extra datasets
    monkeypatch.setenv(
        "DATASETS_LIST_DIR",
        str(Path(__file__).parent.parent.parent / "unittest" / "mock_data"),
    )


@pytest.fixture
def path_to_mock_original_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "original_recipe_radiation_budget.yml"
    )
    return path


@pytest.fixture
def path_to_blank_recipe_kgo():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "blank_recipe_radiation_budget.yml"
    )
    return path


@pytest.fixture
def path_to_updated_recipe_kgo():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "updated_recipe_radiation_budget.yml"
    )
    return path


@pytest.fixture
def path_to_kgo_extended_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "extended_radiation_budget_recipe.yml"
    )
    return path


@pytest.fixture
def path_to_cmip6_datasets_yaml():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "cmip6_datasets.yml"
    )
    return path



def test_return_blank_recipe(
    path_to_blank_recipe_kgo, path_to_mock_original_recipe
):
    with open(path_to_blank_recipe_kgo, "r") as file_handle:
        expected = yaml.safe_load(file_handle)
    actual = return_blank_recipe(path_to_mock_original_recipe)
    assert actual == expected


def test_add_extra_datasets(
    path_to_updated_recipe_kgo,
        path_to_cmip6_datasets_yaml,
    path_to_kgo_extended_recipe,
):
    with open(path_to_kgo_extended_recipe, "r") as file_handle_1:
        expected = yaml.safe_load(file_handle_1)

    with open(path_to_updated_recipe_kgo, "r") as file_handle_2:
        pre_recipe = yaml.safe_load(file_handle_2)

    # Using str(filepath) here as update_recipe_file.py uses os, not pathlib
    actual = add_extra_datasets(pre_recipe, str(path_to_cmip6_datasets_yaml))
    assert actual == expected


def test_main(
    monkeypatch,
    mock_env_vars,
    path_to_kgo_extended_recipe,
    path_to_mock_original_recipe,
    tmp_path,
):
    """main() should overwrite the recipe in-place with the updated content."""
    # Copy the original recipe to a tmp_path location to allow it to be
    # overwritten.
    path_to_temp_recipe = tmp_path / "tmp_recipe.yml"
    shutil.copy(path_to_mock_original_recipe, path_to_temp_recipe)

    # Mock the environmental variable 'RECIPE PATH' to the tmp_path location
    # where the original recipe is stored.
    monkeypatch.setenv("RECIPE_PATH", str(path_to_temp_recipe))

    main()

    with open(path_to_temp_recipe, "r") as file_handle_1:
        actual_lines = file_handle_1.readlines()

    with open(path_to_kgo_extended_recipe, "r") as file_handle_2:
        kgo_with_comment = file_handle_2.readlines()

    # Remove the five comment lines at the top of
    # 'updated_recipe_radiation_budget.yml'.
    kgo_without_comment = kgo_with_comment[5:]

    assert actual_lines == kgo_without_comment
