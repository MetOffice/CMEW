#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Overwrite the ESMValTool recipe with an updated version. Include:

* CMEW required values
* User configurable variables from the Rose suite configuration
"""
import os
import yaml


def return_blank_recipe(recipe_path):
    """Empty the datasets section of an ESMValTool recipe.

    Parameters
    ----------
    recipe_path: str
        Location of the ESMValTool recipe file.

    Returns
    -------
    recipe: dict
        The content of the ESMValTool recipe with an empty datasets section.
    """
    with open(recipe_path, "r") as file_handle:
        recipe = yaml.safe_load(file_handle)

    # Empty the datasets section of the recipe
    recipe["datasets"] = []

    return recipe


def add_extra_datasets(recipe, yaml_filepath):
    """
    Parameters
    ----------
    recipe: dict
        The content of the ESMValTool recipe to which datasets are to be added.
    yaml_filepath: str
        The location of the YAML file containing the extra datasets.

    Returns
    -------
    recipe: dict
        The content of the ESMValTool recipe with an extended datasets section.
    """
    # Read the extra datasets from the provided YAML file
    with open(yaml_filepath, "r") as file_handle:
        extra_datasets = yaml.safe_load(file_handle)

    # ESMValTool recipes expect keys to be "dataset", "ensemble", "exp" etc.
    variables_conversion = {
        "label_for_plots": "alias",
        "model_id": "dataset",
        "variant_label": "ensemble",
        "experiment_id": "exp",
    }

    # Some attributes are neither needed nor wanted by ESMValTool
    unwanted_keys = ["calendar", "suite_id"]

    # Convert the variable names in the extra datasets
    for dataset, inner_dict in extra_datasets.items():
        for key in unwanted_keys:
            if key in inner_dict:
                del inner_dict[key]
        for old_key, new_key in variables_conversion.items():
            if old_key in inner_dict:
                inner_dict[new_key] = inner_dict.pop(old_key)

    # Collect the new inner dicts to append to datasets section of the recipe
    extra_datasets_list = list(extra_datasets.values())

    # Add the datasets to the datasets section of the recipe
    recipe["datasets"].extend(extra_datasets_list)

    return recipe


def write_recipe(updated_recipe, target_path):
    """Write updated ESMValTool recipe to a YAML file at ``target_path``.

    Parameters
    ----------
    updated_recipe: dict
        Dictionary containing the updated ESMValTool recipe content.

    target_path: str
        Location to write the updated ESMValTool recipe.
    """
    with open(target_path, "w") as file_handle:
        yaml.dump(
            updated_recipe,
            file_handle,
            default_flow_style=False,
            sort_keys=True,
        )


def main():
    """
    Load and update the ESMValTool recipe. Overwrite the original recipe with
    the updated recipe.
    """
    recipe_path = os.environ["RECIPE_PATH"]
    blank_recipe = return_blank_recipe(recipe_path)

    # Add the model runs into the datasets section of the recipe
    model_runs_fp = f"{os.environ['DATASETS_LIST_DIR']}/model_runs.yml"
    updated_recipe = add_extra_datasets(blank_recipe, model_runs_fp)

    # Add the CMIP6 datasets to the recipe
    cmip6_datasets_fp = f"{os.environ['DATASETS_LIST_DIR']}/cmip6_datasets.yml"
    extended_recipe = add_extra_datasets(updated_recipe, cmip6_datasets_fp)

    write_recipe(extended_recipe, recipe_path)


if __name__ == "__main__":
    main()
