# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
from update_recipe_file import update_recipe
from pathlib import Path
import yaml


def test_update_recipe(monkeypatch):
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")

    updated_recipe_kgo_path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "kgo"
        / "test_updated_recipe.yml"
    )

    with open(updated_recipe_kgo_path, "r") as f:
        expected = yaml.safe_load(f)

    original_recipe_path = (
        Path(__file__).parent.parent.parent
        / "unittest"
        / "mock_data"
        / "test_recipe.yml"
    )
    actual = update_recipe(original_recipe_path)

    assert actual == expected
