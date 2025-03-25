#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Overwrite the ESMValTool recipe with an updated version. Include:

* CMEW required values
* User configurable variables from the Rose suite configuration
"""
import os
import argparse
import yaml


def update_recipe(recipe_path, variant_label):
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
    variant_label: str
        The ensemble/variant of a test or reference model.

    Returns
    -------
    recipe: dict[str, union[str, int]]
        The content of the ESMValTool recipe with updated datasets section.
    """
    start_year = int(os.environ["START_YEAR"])
    end_year = (
        int(os.environ["START_YEAR"]) + int(os.environ["NUMBER_OF_YEARS"]) - 1
    )
    with open(recipe_path, "r") as file_handle:
        recipe = yaml.safe_load(file_handle)
    first_dataset = recipe["datasets"][0]
    second_dataset = recipe["datasets"][1]
    first_dataset.update({"start_year": start_year, "end_year": end_year})
    second_dataset.update(
        {
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": variant_label,
            "start_year": start_year,
            "end_year": end_year,
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


def main(recipe_path, variant_label):
    """
    Load and update the ESMValTool recipe. Overwrite the original recipe with
    the updated recipe.

    Parameters
    ----------
    recipe_path: str
        Path to the recipe file.
    variant_label: str
        Ensemble/Variant label.
    """
    updated_recipe = update_recipe(recipe_path, variant_label)
    write_recipe(updated_recipe, recipe_path)


if __name__ == "__main__":
    # Get args from cmd line.  This needs to be told which of test or reference
    # settings to use, it cannot decide itself.
    parser = argparse.ArgumentParser(
        prog="Update-recipe-file",
        description="Update a recipe file for a test or reference model.",
    )
    parser.add_argument("-p", help="Recipe path", required=True)
    parser.add_argument("-v", help="Variant Label", required=True)
    args = parser.parse_args()

    main(args.p, args.v)
