#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
import os
import yaml


def update_recipe(recipe_path):
    start_year = int(os.environ["START_YEAR"])
    end_year = (
        int(os.environ["START_YEAR"]) + int(os.environ["NUMBER_OF_YEARS"]) - 1
    )
    with open(recipe_path, "r") as f:
        recipe = yaml.safe_load(f)
    first_dataset = recipe["datasets"][0]
    second_dataset = recipe["datasets"][1]
    first_dataset.update({"start_year": start_year, "end_year": end_year})
    second_dataset.update(
        {
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": "r1i1p1f1",
            "start_year": start_year,
            "end_year": end_year,
        }
    )
    return recipe


def write_recipe(updated_recipe, target_path):
    with open(target_path, "w") as f:
        yaml.dump(updated_recipe, f)


def main():
    recipe_path = os.environ["RECIPE_PATH"]
    updated_recipe = update_recipe(recipe_path)
    write_recipe(updated_recipe, recipe_path)


if __name__ == "__main__":
    main()
