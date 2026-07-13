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
    recipe_content: dict
        The content of the ESMValTool recipe with an empty datasets section.
    """
    with open(recipe_path, "r") as file_handle:
        recipe_content = yaml.safe_load(file_handle)

    # Empty the datasets section of the recipe
    logger.debug("Emptying datasets from %s", recipe_path)
    recipe_content["datasets"] = []

    return recipe_content


def add_extra_datasets(recipe_content, yaml_filepath):
    """
    Adds all datasets listed in a YAML file to an ESMValTool recipe.

    Changes are made to the names and existence of some keys.

    Parameters
    ----------
    recipe_content: dict
        The content of the ESMValTool recipe to which to add datasets.
    yaml_filepath: str
        The location of the YAML file containing the extra datasets.

    Returns
    -------
    recipe_content: dict
        The content of the ESMValTool recipe
        with an extended datasets section.
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
    recipe_content["datasets"].extend(extra_datasets_list)

    return recipe_content


def remove_additional_datasets(recipe_content, recipe_id, recipe_dict_fp):
    """
    Optionally remove additional_datasets sections from an ESMValTool recipe.

    The option to remove additional datasets is controlled by the key
    empty_additional_datasets in the YAML file at RECIPE_DICT_PATH.

    Parameters
    ----------
    recipe_content: dict
        The content of the recipe which may have additional datasets.
    recipe_id: str
        The id that acts as a key in the recipe_dict_fp.
    recipe_dict_fp: str
        The location of the YAML file containing information
        about whether to remove additional datasets.

    Returns
    -------
    recipe_content: dict
        The content of the recipe which may be unchanged
        or may have had additional_datasets removed.
    """
    # Load the yaml config file from ../etc
    logger.debug("Reading recipe dict from %s", recipe_dict_fp)
    with open(recipe_dict_fp, "r") as f:
        recipe_dict = yaml.safe_load(f)
    logger.debug("Recipe dict:\n%s", recipe_dict)

    # Don't empty by default
    empty_additionals = False

    # Read specific recipe names and filepaths from the yaml config file
    if recipe_id in recipe_dict:
        logger.debug("Using info from recipe dictionary for %s", recipe_id)
        if "empty_additional_datasets" in recipe_dict[recipe_id]:

            # Assign True if specified in YAML file (boolean)
            empty_additionals = recipe_dict[recipe_id][
                "empty_additional_datasets"
            ]

    # Empty from recipe if specified
    if empty_additionals:
        for diag in recipe_content["diagnostics"]:
            for var in recipe_content["diagnostics"][diag]["variables"]:
                del recipe_content["diagnostics"][diag]["variables"][var][
                    "additional_datasets"
                ]

    logger.debug("Updated recipe content:\n%s", recipe_content)
    return recipe_content


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


def update_recipe_file(
    recipe_path,
    model_runs_yml_fp,
    cmip6_datasets_yml_fp,
    recipe_id,
    recipe_dict_fp,
):
    """
    Update the datasets in an ESMValTool recipe.

    Overwrite the original recipe content with the updated recipe content.

    Parameters
    ----------
    recipe_path:
        The filepath of the ESMValTool recipe to be updates.
    model_runs_yml_fp:
        The full path to the YAML file containing details of the model runs.
    cmip6_datasets_yml_fp:
        The full path to the YAML file containing details of the CMIP6
        datasets to include.
    recipe_id:
        The id that acts as a key in the recipe_dict_fp.
    recipe_dict_fp:
        The location of the YAML file containing information
        about whether to remove additional datasets.
    """
    blank_recipe = return_blank_recipe(recipe_path)
    logger.info("Amending recipe from %s", recipe_path)

    # Remove additional datasets if specified
    amended_recipe = remove_additional_datasets(
        blank_recipe, recipe_id, recipe_dict_fp
    )

    # Add the model runs into the datasets section of the recipe
    logger.info("Adding model runs to recipe")
    updated_recipe = add_extra_datasets(amended_recipe, model_runs_yml_fp)

    # Add the CMIP6 datasets to the recipe
    logger.info("Adding CMIP6 runs to recipe")
    extended_recipe = add_extra_datasets(updated_recipe, cmip6_datasets_yml_fp)

    write_recipe(extended_recipe, recipe_path)
