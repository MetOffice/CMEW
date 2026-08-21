#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Update the datasets in an ESMValTool recipe. Include:

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


def load_yaml(file_path):
    """
    Return the contents of the YAML file.

    Parameters
    ----------
    file_path : str
        The full path to the YAML file.

    Returns
    -------
    : dict
        The contents of the YAML file.
    """
    logger.debug(f"Loading {file_path}")
    with open(file_path, "r") as file_handle:
        contents = yaml.safe_load(file_handle)

    return contents


def remove_datasets_contents(recipe):
    """
    Return the contents of an ESMValTool recipe
    with an empty ``datasets`` section.

    Parameters
    ----------
    recipe : dict
        The contents of an ESMValTool recipe.

    Returns
    -------
    : dict
        The content of an ESMValTool recipe
        with an empty ``datasets`` section.
    """
    logger.debug("Emptying the 'datasets' section in the ESMValTool recipe")
    recipe["datasets"] = []

    return recipe


def remove_additional_datasets(recipe):
    """
    Return the contents of an ESMValTool recipe
    with any ``additional_datasets`` removed.

    Parameters
    ----------
    recipe : dict
        The contents of an ESMValTool recipe
        that may have additional datasets.

    Returns
    -------
    : dict
        The content of an ESMValTool recipe
        with any ``additional_datasets`` removed.
    """
    logger.debug("Removing additional datasets in the ESMValTool recipe")
    for diagnostic in recipe["diagnostics"]:
        for variable in recipe["diagnostics"][diagnostic]["variables"]:
            del recipe["diagnostics"][diagnostic]["variables"][variable][
                "additional_datasets"
            ]

    return recipe


def construct_datasets_contents(datasets):
    """
    Return the contents of a ``datasets`` section
    for an ESMValTool recipe.

    Parameters
    ----------
    datasets : list of dict
        The datasets to format for the ``datasets`` section in the form:
        [{suite_id_1: {<dataset_1>}, {model_id_2: {<dataset_2>}, ...].

    Returns
    -------
    : dict
        The contents of a ``datasets`` sections
        for an ESMValTool recipe.
    """
    logger.debug("Constructing the contents of the ``datasets`` section")

    # ESMValTool recipes expect keys to be "dataset", "ensemble", "exp", etc.
    cmew_to_esmvaltool_key_mapping = {
        "label_for_plots": "alias",
        "model_id": "dataset",
        "variant_label": "ensemble",
        "experiment_id": "exp",
    }

    # Some attributes are neither needed nor wanted by ESMValTool.
    unwanted_keys = ["calendar", "suite_id"]

    # Update the keys in the datasets, as appropriate.
    datasets_for_recipe = []
    for dataset in datasets:
        for identifier, dataset_items in dataset.items():
            for key in unwanted_keys:
                if key in dataset_items:
                    del dataset_items[key]
            for old_key, new_key in cmew_to_esmvaltool_key_mapping.items():
                if old_key in dataset_items:
                    dataset_items[new_key] = dataset_items.pop(old_key)
            datasets_for_recipe.append(dataset_items)

    return datasets_for_recipe


def add_datasets_contents(recipe, datasets):
    """
    Return the contents of a ESMValTool recipe
    with a complete ``datasets`` section.

    Parameters
    ----------
    recipe : dict
        The contents of an ESMValTool recipe.
    datasets : dict
        The datasets to be added to the ESMValTool recipe.

    Returns
    -------
    : dict
        The contents of a valid ESMValTool recipe.
    """
    # Add the datasets to the 'datasets' section
    # of the ESMValTool recipe.
    logger.debug("Adding the datasets to the ESMValTool recipe")
    recipe["datasets"] = datasets

    return recipe


def write_yaml(contents, target_path):
    """
    Write the contents to a YAML file at ``target_path``.

    Parameters
    ----------
    contents : dict
        The contents to write to the YAML file.
    target_path : str
        The full path to write the YAML file.
    """
    with open(target_path, "w") as file_handle:
        yaml.dump(
            contents,
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
        The full path to the ESMValTool recipe.
    model_runs_yml_fp:
        The full path to the YAML file containing details of the model runs.
    cmip6_datasets_yml_fp:
        The full path to the YAML file containing details of the CMIP6
        datasets to include.
    recipe_id:
        The id that acts as a key in the recipe_dict_fp.
    recipe_dict_fp:
        The full path to the YAML file containing information
        about whether to remove additional datasets.
    """
    recipe = load_yaml(recipe_path)
    model_runs = load_yaml(model_runs_yml_fp)
    cmip6_datasets = load_yaml(cmip6_datasets_yml_fp)

    recipe = remove_datasets_contents(recipe)
    if recipe_id == "correlation":
        recipe = remove_additional_datasets(recipe)

    datasets = construct_datasets_contents([model_runs, cmip6_datasets])
    recipe = add_datasets_contents(recipe, datasets)

    write_yaml(recipe, recipe_path)
