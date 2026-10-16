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

# Annual/monthly routing is controlled by the model run's
# "standardisation_frequency" facet. The native archive source is
# independent: both monthly Omon and annual Oyr routes may use "onm".
ANNUAL_STANDARDISATION_FREQUENCY = "annual"


def is_annual_source(run):
    """
    Return whether a model run requests annual standardisation.

    Parameters
    ----------
    run : dict
        A model run dict, as read from model_runs.yml.

    Returns
    -------
    bool
        True if "standardisation_frequency" is "annual".
    """
    return (
        run.get("standardisation_frequency")
        == ANNUAL_STANDARDISATION_FREQUENCY
    )


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


def remove_extract_time(recipe):
    """
    Remove fixed ``extract_time`` settings from recipe preprocessors.

    CMEW supplies the evaluation period through the configured model
    datasets, so the ocean quadmap recipe must not impose the upstream
    recipe's fixed analysis period.
    """
    logger.debug("Removing fixed extract_time settings from preprocessors")
    for preprocessor in recipe.get("preprocessors", {}).values():
        preprocessor.pop("extract_time", None)

    return recipe


def update_ocean_quadmap_model_selectors(recipe, model_runs):
    """
    Update ocean quadmap control and experiment model selectors.

    The upstream recipe hard-codes specific CMIP6 models. CMEW instead
    derives these selectors from the configured model runs, using the
    run marked ``benchmark_dataset`` as the control model.
    """
    control_runs = [
        run
        for run in model_runs.values()
        if run.get("benchmark_dataset", False)
    ]
    experiment_runs = [
        run
        for run in model_runs.values()
        if not run.get("benchmark_dataset", False)
    ]

    if len(control_runs) != 1 or len(experiment_runs) != 1:
        raise ValueError(
            "ocean_quadmap requires exactly one benchmark/control model "
            "and exactly one experiment model"
        )

    def model_selector(run):
        # The ony archive convention labels the annual record by the
        # calendar year containing its midpoint, one year after the
        # configured start year (e.g. configured 1850 -> Oyr year 1851),
        # so annual CMEW datasets must use mip: Oyr here to match the
        # corresponding generated dataset entry.
        mip = "Oyr" if is_annual_source(run) else "Omon"
        return {
            "dataset": run["model_id"],
            "ensemble": run["variant_label"],
            "exp": run["experiment_id"],
            "mip": mip,
            "project": run["project"],
        }

    control_model = model_selector(control_runs[0])
    exper_model = model_selector(experiment_runs[0])

    # Update every instance of the ocean quadmap diagnostic rather than
    # relying on YAML anchor behaviour from the upstream recipe.
    for diagnostic in recipe.get("diagnostics", {}).values():
        for script in diagnostic.get("scripts", {}).values():
            if script.get("script") == "ocean/diagnostic_maps_quad.py":
                script["control_model"] = control_model.copy()
                script["exper_model"] = exper_model.copy()

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

    # ESMValTool recipes expect keys to have the values on the right.
    cmew_to_esmvaltool_key_mapping = {
        "label_for_plots": "alias",
        "model_id": "dataset",
        "variant_label": "ensemble",
        "experiment_id": "exp",
    }

    # Some attributes are neither needed nor wanted by ESMValTool.
    unwanted_keys = [
        "calendar",
        "suite_id",
        "archive_stream",
        "standardisation_frequency",
    ]

    # Update the keys in the datasets, as appropriate.
    datasets_for_recipe = []
    for dataset in datasets:
        for dataset_items in dataset.values():
            # Datasets requesting annual standardisation need an
            # explicit per-dataset "mip: Oyr" override so this dataset
            # alone deviates from the recipe's default "mip: Omon"
            # variable declaration. The new annual route derives true
            # calendar-year means from monthly onm input, so no year
            # offset is required.
            if is_annual_source(dataset_items):
                dataset_items["mip"] = "Oyr"
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
):
    """
    Update the datasets in an ESMValTool recipe.

    Overwrite the original recipe content
    with the updated recipe content.

    Parameters
    ----------
    recipe_path:
        The full path to the ESMValTool recipe.
    model_runs_yml_fp:
        The full path to the YAML file
        containing details of the model datasets to include.
    cmip6_datasets_yml_fp:
        The full path to the YAML file
        containing details of the CMIP6 datasets to include.
    recipe_id:
        The identifier that determines
        whether additional datasets should be removed.
    """
    recipe = load_yaml(recipe_path)
    model_runs = load_yaml(model_runs_yml_fp)
    cmip6_datasets = load_yaml(cmip6_datasets_yml_fp)

    recipe = remove_datasets_contents(recipe)
    if recipe_id == "correlation":
        recipe = remove_additional_datasets(recipe)
    if recipe_id == "ocean_quadmap":
        # The upstream recipe fixes the analysis period to 2000-2003,
        # which is incompatible with CMEW's user-configured model period.
        recipe = remove_extract_time(recipe)

        # Replace the upstream hard-coded model selectors with selectors
        # derived from the model runs configured for this CMEW workflow.
        recipe = update_ocean_quadmap_model_selectors(recipe, model_runs)

    datasets = construct_datasets_contents([model_runs, cmip6_datasets])
    recipe = add_datasets_contents(recipe, datasets)

    write_yaml(recipe, recipe_path)
