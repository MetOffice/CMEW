# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
from update_recipe_file import update_recipe, main
from pathlib import Path
import pytest
import shutil
import yaml


@pytest.fixture
def mock_env_vars(monkeypatch):
    # Time window
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("LABEL_FOR_PLOTS", "Test Label")
    monkeypatch.setenv("REF_LABEL_FOR_PLOTS", "Ref Test Label")

    # Reference run metadata
    monkeypatch.setenv("REF_MODEL_ID", "HadGEM3-GC31-LL")
    monkeypatch.setenv("REF_VARIANT_LABEL", "r1i1p1f3")

    # Evaluation run metadata
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("VARIANT_LABEL", "r1i1p1f1")


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
    """update_recipe should produce the KGO with both datasets updated.

    - Dataset[0] uses REF_MODEL_ID / REF_VARIANT_LABEL
    - Dataset[1] uses MODEL_ID / VARIANT_LABEL
    - start_year and end_year are set from START_YEAR / NUMBER_OF_YEARS
    """
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

    with open(path_to_updated_recipe_kgo, "r") as file_handle_2:
        kgo_with_comment = file_handle_2.readlines()

    # Remove the five comment lines at the top of
    # 'test_updated_radiation_budget_recipe.yml'.
    kgo_without_comment = kgo_with_comment[5:]

    assert actual_lines == kgo_without_comment
