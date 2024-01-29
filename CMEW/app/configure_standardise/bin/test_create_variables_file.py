#!/usr/bin/env python
"""
Tests for configure_standardise
"""
from create_variables_file import parse_variables_from_recipe
from pathlib import Path


def test_parse_radiation_budget_variables():
    recipe_path = (
        Path(__file__).parent.parent / "mock_data" / "test_recipe.yml"
    )
    actual = parse_variables_from_recipe(recipe_path)
    expected = """Emon/rss
Amon/rsdt
Amon/rsut
Amon/rsutcs
Amon/rsds
Emon/rls
Amon/rlut
Amon/rlutcs
Amon/rlds
Amon/hfss
Amon/hfls
"""
    assert actual == expected
