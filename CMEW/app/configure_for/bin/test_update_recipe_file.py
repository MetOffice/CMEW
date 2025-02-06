# (C) Crown Copyright 2024-2025, Met Office.
# Please see LICENSE.md for license details.
from update_recipe_file import update_recipe, main
from pathlib import Path
import pytest
import shutil
import yaml


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")


@pytest.fixture
def path_to_updated_recipe_kgo():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "test_updated_radiation_budget_recipe.yml"
    )
    return path


@pytest.fixture
def path_to_mock_original_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "test_radiation_budget_recipe_v2.9.0.yml"
    )
    return path


def test_update_recipe(
    mock_env_vars, path_to_updated_recipe_kgo, path_to_mock_original_recipe
):
    with open(path_to_updated_recipe_kgo, "r") as file_handle:
        expected = yaml.safe_load(file_handle)
    actual = update_recipe(path_to_mock_original_recipe)
    assert actual == expected


def test_main(
    monkeypatch,
    mock_env_vars,
    path_to_updated_recipe_kgo,
    path_to_mock_original_recipe,
    tmp_path,
):
    # Copy the original recipe to a tmp_path location to allow it to be
    # overwritten.
    path_to_temp_recipe = tmp_path / "tmp_recipe.yml"
    shutil.copy(path_to_mock_original_recipe, path_to_temp_recipe)

    # Mock the environmental variable 'RECIPE PATH' to the tmp_path location
    # where the original recipe is stored.
    monkeypatch.setenv("RECIPE_PATH", path_to_temp_recipe)

    main()

    with open(path_to_temp_recipe, "r") as file_handle_1:
        actual = file_handle_1.readlines()

    with open(path_to_updated_recipe_kgo, "r") as file_handle_2:
        kgo_with_comment = file_handle_2.readlines()

    # Remove the three line comment at the top of
    # 'test_updated_radiation_budget_recipe.yml'.
    kgo_without_comment = kgo_with_comment[5:]

    assert actual == kgo_without_comment
