#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Update datasets in an ESMValTool recipe."""
import logging
import os
import sys
from typing import Any

import yaml

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def load_yaml(file_path: str) -> dict[str, Any]:
    """Load YAML contents from ``file_path``."""
    logger.debug("Loading %s", file_path)
    with open(file_path, "r", encoding="utf-8") as file_handle:
        return yaml.safe_load(file_handle)


def remove_datasets_contents(recipe: dict[str, Any]) -> dict[str, Any]:
    """Clear the recipe's datasets section before rebuilding it."""
    logger.debug("Emptying the recipe datasets section")
    recipe["datasets"] = []
    return recipe


def remove_additional_datasets(recipe: dict[str, Any]) -> dict[str, Any]:
    """Remove additional datasets from recipe variables."""
    logger.debug("Removing additional datasets from the recipe")
    for diagnostic in recipe["diagnostics"].values():
        for variable in diagnostic["variables"].values():
            variable.pop("additional_datasets", None)
    return recipe


def construct_datasets_contents(
    datasets: list[dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Convert CMEW model metadata to ESMValTool dataset entries."""
    logger.debug("Constructing ESMValTool dataset entries")
    key_mapping = {
        "label_for_plots": "alias",
        "model_id": "dataset",
        "variant_label": "ensemble",
        "experiment_id": "exp",
    }
    unwanted_keys = ["calendar", "suite_id"]
    recipe_datasets = []
    for dataset_group in datasets:
        for dataset in dataset_group.values():
            for key in unwanted_keys:
                dataset.pop(key, None)
            for old_key, new_key in key_mapping.items():
                if old_key in dataset:
                    dataset[new_key] = dataset.pop(old_key)
            recipe_datasets.append(dataset)
    return recipe_datasets


def add_datasets_contents(
    recipe: dict[str, Any], datasets: list[dict[str, Any]]
) -> dict[str, Any]:
    """Set the recipe's datasets section."""
    logger.debug("Adding datasets to the recipe")
    recipe["datasets"] = datasets
    return recipe


def write_yaml(contents: dict[str, Any], target_path: str) -> None:
    """Write YAML contents to ``target_path``."""
    with open(target_path, "w", encoding="utf-8") as file_handle:
        yaml.dump(
            contents,
            file_handle,
            default_flow_style=False,
            sort_keys=True,
        )


def update_recipe_file(
    recipe_path: str,
    model_runs_yml_fp: str,
    cmip6_datasets_yml_fp: str,
    recipe_id: str,
) -> None:
    """Replace recipe datasets with configured model and CMIP6 datasets."""
    recipe = load_yaml(recipe_path)
    model_runs = load_yaml(model_runs_yml_fp)
    cmip6_datasets = load_yaml(cmip6_datasets_yml_fp)

    recipe = remove_datasets_contents(recipe)
    if recipe_id == "correlation":
        recipe = remove_additional_datasets(recipe)

    datasets = construct_datasets_contents([model_runs, cmip6_datasets])
    recipe = add_datasets_contents(recipe, datasets)
    write_yaml(recipe, recipe_path)
