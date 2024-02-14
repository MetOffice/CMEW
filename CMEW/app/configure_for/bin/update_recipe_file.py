#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
import os
import yaml


def update_recipe(recipe_path):
    with open(recipe_path, "r") as f:
        original_recipe = yaml.safe_load(f)
    updated_recipe = original_recipe
    return updated_recipe


def write_recipe(recipe, target_path):
    with open(target_path, "w") as f:
        yaml.dump(recipe, f)


def main():
    recipe_path = os.environ["RECIPE_NAME"]
    updated_recipe = update_recipe(recipe_path)
    write_recipe(updated_recipe, recipe_path)


if __name__ == "__main__":
    main()

    # FOR QUICK PYYAML TESTS
    # with open('/net/home/h02/cbillows/Code/CMEW/CMEW/app/configure_for/recipe_data/recipe_radiation_budget.yml', 'r') as file: # noqa: E501
    #     data = yaml.safe_load(file)
    # print(data)
