#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
import subprocess
import yaml
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def retrieve_name_and_fp():
    """
    Looks in recipe_paths.yml for an entry or constructs default values.

    Uses the environment variable CYLC_TASK_PARAM_recipe as a dict key.

    Returns
    -------
    recipe_name: str
        The name of the recipe, usually of the form recipe_thing.yml
    recipe_fp: str
        The location of the recipe withing esmvaltool/recipes

    """
    # Look up the recipe and destination from the environment
    recipe = os.environ["CYLC_TASK_PARAM_recipe"]
    logger.info("Fetching recipe %s", recipe)

    # Load the yaml config file from ../etc
    recipe_dict_fp = os.environ["RECIPE_DICT_PATH"]
    logger.debug("Reading recipe dict from %s", recipe_dict_fp)
    with open(recipe_dict_fp, "r") as f:
        recipe_dict = yaml.safe_load(f)
    logger.debug("Recipe dict:\n%s", recipe_dict)

    # Read specific recipe names and filepaths from the yaml config file
    if recipe in recipe_dict:
        logger.debug("Using info from recipe dictionary for %s", recipe)
        recipe_name = recipe_dict[recipe]["recipe_name"]
        recipe_fp = recipe_dict[recipe]["recipe_fp"]

    # Or use the defaults
    else:
        logger.debug("Using default name and filepath for recipe %s", recipe)
        recipe_name = f"recipe_{recipe}.yml"
        recipe_fp = recipe_name

    return recipe_name, recipe_fp


def main():
    """Fetch a recipe from ESMValTool and copy it to the recipe path."""
    # Find the full name and location within ESMValTool
    recipe_name, recipe_fp = retrieve_name_and_fp()

    # Look up final destination
    destination_fp = os.environ["RECIPE_PATH"]
    logger.info("Recipe will be written to %s", destination_fp)

    # Build the command to fetch and move the recipe
    command = f"""
    cmew-esmvaltool-env esmvaltool recipes get {recipe_fp}
    mv {recipe_name} {destination_fp}
    """

    # Run the command
    logging.info("Running command: %s", command)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
