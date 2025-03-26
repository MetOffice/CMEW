# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
from update_recipe_file import update_recipe, main
from pathlib import Path
import pytest
import shutil
import yaml

variant_label = "r1i1p1f1"  # = ensemble


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
    mock_env_vars,
    path_to_updated_recipe_kgo,
    path_to_mock_original_recipe,  # noqa : 36
):
    with open(path_to_updated_recipe_kgo, "r") as file_handle:
        expected = yaml.safe_load(file_handle)
    actual = update_recipe(path_to_mock_original_recipe, variant_label)
    assert actual == expected


def test_main(
    mock_env_vars,  # noqa : 36
    path_to_updated_recipe_kgo,
    path_to_mock_original_recipe,
    tmp_path,
):
    # Copy the original recipe to a tmp_path location to allow it to be
    # overwritten.
    path_to_temp_recipe = tmp_path / "tmp_recipe.yml"
    shutil.copy(path_to_mock_original_recipe, path_to_temp_recipe)

    main(path_to_temp_recipe, variant_label)

    with open(path_to_temp_recipe, "r") as file_handle_1:
        actual = file_handle_1.readlines()

    with open(path_to_updated_recipe_kgo, "r") as file_handle_2:
        kgo_with_comment = file_handle_2.readlines()

    # Remove the five comment lines at the top of
    # 'test_updated_radiation_budget_recipe.yml'.
    kgo_without_comment = kgo_with_comment[5:]

    assert actual == kgo_without_comment
