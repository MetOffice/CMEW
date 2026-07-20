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
import sys
import logging
from config_configure_for import recipes_dict

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


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
    logger.debug("Emptying datasets from %s", recipe_path)
    recipe["datasets"] = []

    return recipe


def add_extra_datasets(recipe, yaml_filepath):
    """
    Adds all datasets listed in a YAML file to an ESMValTool recipe.

    Changes are made to the names and existence of some keys.

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
    logger.debug("Processing extra datasets:\n%s", extra_datasets)

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
    logger.debug("Adding extra datasets:\n%s", extra_datasets_list)
    recipe["datasets"].extend(extra_datasets_list)

    return recipe


def remove_additional_datasets(recipe, recipe_dict=recipes_dict):
    """
    Optionally remove additional_datasets sections from an ESMValTool recipe.

    The option to remove additional datasets is controlled by the key
    empty_additional_datasets in the recipe_dict.

    Parameters
    ----------
    recipe: dict
        The content of the recipe which may have additional datasets.
    recipe_dict : dict
        A dictionary with keys for a recipe identifier and the value
        True assigned to an inner key of empty_additional_datasets
        if additional datasets are to be emptied from a recipe.

    Returns
    -------
    recipe: dict
        The content of the recipe which may be unchanged
        or may have had additional_datasets removed.
    """
    # Look up the recipe and destination from the environment
    recipe_id = os.environ["CYLC_TASK_PARAM_recipe"]

    # Don't empty by default
    empty_additionals = False

    # Read specific recipe names and filepaths from the config file
    logger.debug("Recipe dict:\n%s", recipe_dict)

    if recipe_id in recipe_dict:
        logger.debug("Using info from recipe dictionary for %s", recipe_id)
        if "empty_additional_datasets" in recipe_dict[recipe_id]:

            # Assign True if specified in YAML file (boolean)
            empty_additionals = recipe_dict[recipe_id][
                "empty_additional_datasets"
            ]

    # Empty from recipe if specified
    if empty_additionals:
        for diag in recipe["diagnostics"]:
            for var in recipe["diagnostics"][diag]["variables"]:
                del recipe["diagnostics"][diag]["variables"][var][
                    "additional_datasets"
                ]

    logger.debug("Updated recipe:\n%s", recipe)
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
    logger.info("Amending recipe from %s", recipe_path)

    # Remove additional datasets if specified
    amended_recipe = remove_additional_datasets(blank_recipe)

    # Add the model runs into the datasets section of the recipe
    model_runs_fp = f"{os.environ['DATASETS_LIST_DIR']}/model_runs.yml"
    logger.info("Adding model runs to recipe")
    updated_recipe = add_extra_datasets(amended_recipe, model_runs_fp)

    # Add the CMIP6 datasets to the recipe
    cmip6_datasets_fp = f"{os.environ['DATASETS_LIST_DIR']}/cmip6_datasets.yml"
    logger.info("Adding CMIP6 runs to recipe")
    extended_recipe = add_extra_datasets(updated_recipe, cmip6_datasets_fp)

    write_recipe(extended_recipe, recipe_path)


if __name__ == "__main__":
    main()
