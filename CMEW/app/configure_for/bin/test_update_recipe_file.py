# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
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
        / "test_updated_recipe.yml"
    )
    return path


@pytest.fixture
def path_to_mock_original_recipe():
    path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "test_recipe.yml"
    )
    return path


def test_update_recipe(
    mock_env_vars, path_to_updated_recipe_kgo, path_to_mock_original_recipe
):
    with open(path_to_updated_recipe_kgo, "r") as f:
        expected = yaml.safe_load(f)
    actual = update_recipe(path_to_mock_original_recipe)
    assert actual == expected


def test_main(
    monkeypatch,
    mock_env_vars,
    path_to_updated_recipe_kgo,
    path_to_mock_original_recipe,
    tmp_path,
):
    # copy original recipe to temp location so it can be overwritten
    path_to_temp_recipe = tmp_path / "tmp_recipe.yml"
    shutil.copy(path_to_mock_original_recipe, path_to_temp_recipe)

    # set env var to temp location of original recipe
    monkeypatch.setenv("RECIPE_PATH", path_to_temp_recipe)

    main()

    with open(path_to_temp_recipe, "r") as f1, open(
        path_to_updated_recipe_kgo, "r"
    ) as f2:
        actual = f1.readlines()
        kgo_with_comment = f2.readlines()

    # remove three line comment from kgo file contents
    kgo_without_comment = kgo_with_comment[3:]

    assert actual == kgo_without_comment
