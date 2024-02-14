#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
import os
import yaml


def update_recipe(recipe_path):
    with open(recipe_path, "r") as f:
        recipe = yaml.safe_load(f)

    first_dataset = recipe["datasets"][0]
    second_dataset = recipe["datasets"][1]

    first_dataset.update({"end_year": 1993})

    second_dataset.update(
        {
            "project": "ESMVal",
            "exp": "amip",
            "activity": "ESMVal",
            "ensemble": "r1i1p1f1",
            "end_year": 1993,
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
    print("I did a run!")
    main()

    # FOR QUICK PYYAML TESTS
    # with open('/net/home/h02/cbillows/Code/CMEW/CMEW/app/configure_for/recipe_data/recipe_radiation_budget.yml', 'r') as file: # noqa: E501
    #     data = yaml.safe_load(file)
    # print(data)
