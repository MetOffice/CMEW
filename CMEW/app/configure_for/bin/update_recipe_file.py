#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
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
    * Update the dataset section of the recipe with a) CMEW required key/values
      and b) user-configurable values from the Rose suite configuration.

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
    - {dataset: <dataset>, end_year: <end_year>, ensemble: <ensemble>,
      end_year: <end_year>, exp: <exp>, grid: <grid>, project: <project>,
      start_year: <start_year>}
    - {activity: <activity>, dataset: <dataset>, end_year: <end_year>,
      ensemble: <ensemble>, exp: <exp>, grid: <grid>, project: <project>,
      start_year: <start_year>}

    Notes
    -----
    The updated recipe includes one additional CMEW required key: "Activity".

    Parameters
    ----------
    recipe_path: str
        Location of the ESMValTool recipe file.

    Returns
    -------
    recipe: dict[str, union[str, int]]
        The content of the ESMValTool recipe with updated datasets section.
    """
    variant_label = os.environ["VARIANT_LABEL"]
    variant_label_reference = os.environ["VARIANT_LABEL_REFERENCE"]
    model_id = os.environ["MODEL_ID"]
    model_id_reference = os.environ["MODEL_ID_REFERENCE"]
    start_year = int(os.environ["START_YEAR"])
    end_year = (
        int(os.environ["START_YEAR"]) + int(os.environ["NUMBER_OF_YEARS"]) - 1
    )
    with open(recipe_path, "r") as file_handle:
        recipe = yaml.safe_load(file_handle)
    first_dataset = recipe["datasets"][0]  # Reference model
    second_dataset = recipe["datasets"][1]  # Test model

    first_dataset.update(
        {
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": variant_label_reference,
            "start_year": start_year,
            "end_year": end_year,
            "dataset": model_id_reference,
        }
    )
    second_dataset.update(
        {
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": variant_label,
            "start_year": start_year,
            "end_year": end_year,
            "dataset": model_id,
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
    Invoke the load and update of the ESMValTool recipe, getting the relevant
    variables from the environment.
    """
    recipe_path = os.environ["RECIPE_PATH"]
    updated_recipe = update_recipe(recipe_path)
    write_recipe(updated_recipe, recipe_path)


if __name__ == "__main__":
    main()
