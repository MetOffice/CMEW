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


def update_recipe(recipe_path):
    """Update the ESMValTool recipe.

    * Read the ESMValTool recipe YAML file from the provided ``recipe_path``
    * Update the datasets section of the recipe with:
      - CMEW required key/values
      - User configurable values from the Rose suite configuration
        for both the reference and evaluation model runs.

    Recipe file/datasets section snippet (human written YAML)::

    datasets:
      - {dataset: <dataset>, project: <project>, exp: <exp>,
         ensemble: <ensemble>, grid: <grid>, start_year: <start_year>,
         end_year: <end_year>}
      - {dataset: <dataset>, project: <project>, exp: <exp>,
         ensemble: <ensemble>, grid: <grid>, start_year: <start_year>,
         end_year: <end_year>}

    Updated recipe file/datasets section snippet (machine written YAML)::

    datasets:
    - {activity: <activity>, alias: <ref_alias>, dataset: <ref_model_id>,
      end_year: <end_year>, ensemble: <ref_variant>, exp: <exp>, grid: <grid>,
      project: <project>, start_year: <start_year>}
    - {activity: <activity>, alias: <alias>, dataset: <eval_model_id>,
      end_year: <end_year>, ensemble: <eval_variant>, exp: <exp>, grid: <grid>,
      project: <project>, start_year: <start_year>}

    Notes
    -----
    The updated recipe includes:
    * Reference dataset (index 0) using REF_MODEL_ID and REF_VARIANT_LABEL
    * Evaluation dataset (index 1) using MODEL_ID and VARIANT_LABEL
    * two additional CMEW required keys: "Activity" and "Alias".

    Parameters
    ----------
    recipe_path: str
        Location of the ESMValTool recipe file.

    Returns
    -------
    recipe: dict
        The content of the ESMValTool recipe with updated datasets section.
    """
    # Time window from environment
    start_year = int(os.environ["START_YEAR"])
    end_year = (
        int(os.environ["START_YEAR"]) + int(os.environ["NUMBER_OF_YEARS"]) - 1
    )

    # Model metadata from environment
    ref_model_id = os.environ["REF_MODEL_ID"]
    ref_variant = os.environ["REF_VARIANT_LABEL"]
    eval_model_id = os.environ["MODEL_ID"]
    eval_variant = os.environ["VARIANT_LABEL"]

    # Read given reference alias or use the suite ID
    if os.environ.get("REF_LABEL_FOR_PLOTS"):
        ref_alias = os.environ["REF_LABEL_FOR_PLOTS"]
    else:
        ref_alias = os.environ["REF_SUITE_ID"]

    # Read given evaluation alias or use the suite ID
    if os.environ.get("LABEL_FOR_PLOTS"):
        alias = os.environ["LABEL_FOR_PLOTS"]
    else:
        alias = os.environ["SUITE_ID"]

    with open(recipe_path, "r") as file_handle:
        recipe = yaml.safe_load(file_handle)

    datasets = recipe.get("datasets", [])
    if len(datasets) < 2:
        raise ValueError(
            "Expected at least two datasets in the recipe, "
            "one for the reference and one for the evaluation run."
        )

    # Reference dataset: treat as a GCModelDev / ESMVal / amip run,
    # using REF_MODEL_ID & REF_VARIANT_LABEL, with the configured time window.
    ref_dataset = datasets[0]
    ref_dataset.update(
        {
            "dataset": ref_model_id,
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": ref_variant,
            "start_year": start_year,
            "end_year": end_year,
            "alias": ref_alias,
        }
    )

    # Evaluation dataset: ESMVal / amip run using MODEL_ID and VARIANT_LABEL
    eval_dataset = datasets[1]
    eval_dataset.update(
        {
            "dataset": eval_model_id,
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": eval_variant,
            "start_year": start_year,
            "end_year": end_year,
            "alias": alias,
        }
    )

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
        yaml.dump(updated_recipe, file_handle, default_flow_style=False)


def main():
    """
    Load and update the ESMValTool recipe. Overwrite the original recipe with
    the updated recipe.
    """
    recipe_path = os.environ["RECIPE_PATH"]
    updated_recipe = update_recipe(recipe_path)
    write_recipe(updated_recipe, recipe_path)


if __name__ == "__main__":
    main()
