#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def recipe_paths_yml_fp():
    return mock_data_dir() / "recipe_paths.yml"


def model_runs_yml_fp():
    return mock_data_dir() / "model_runs.yml"


def cmip6_datasets_yml_fp():
    return mock_data_dir() / "cmip6_datasets.yml"


def original_recipe_radiation_budget_fp():
    return mock_data_dir() / "original_recipe_radiation_budget.yml"


def recipe_with_additional_datasets_yml_fp():
    return mock_data_dir() / "recipe_with_additional_datasets.yml"


def updated_recipe_radiation_budget_yml_fp():
    return mock_data_dir() / "updated_recipe_radiation_budget.yml"


def kgo_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "kgo"


def no_ds_in_recipe_fp():
    return kgo_dir() / "blank_recipe_radiation_budget.yml"


def recipe_additional_datasets_removed_yml_fp():
    return kgo_dir() / "recipe_additional_datasets_removed.yml"


def extended_radiation_budget_recipe_yml_fp():
    return kgo_dir() / "extended_radiation_budget_recipe.yml"
