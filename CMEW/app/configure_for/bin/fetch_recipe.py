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


def retrieve_name_and_fp(recipe_id, recipe_dict_fp):
    """
    Return the name of a recipe and its location within
    ``esmvaltool/recipes``.

    Parameters
    ----------
    recipe_id : str
        The short identifier of the recipe to retrieve,
        as written in the `flow.cylc` file.
    recipe_dict_fp : str
        The filepath of the YAML file containing the name and location
        within esmvaltool.recipes of the recipe to be fetched.

    Returns
    -------
    recipe_name: str
        The name of the recipe, usually of the form recipe_thing.yml
    recipe_internal_loc: str
        The location of the recipe within esmvaltool/recipes

    """
    logger.info("Fetching recipe %s", recipe_id)

    # Load the yaml config file from ../etc
    with open(recipe_dict_fp, "r") as f:
        recipe_dict = yaml.safe_load(f)
    logger.debug("Recipe dict:\n%s", recipe_dict)

    # Read specific recipe names and filepaths from the yaml config file
    if recipe_id in recipe_dict:
        logger.debug("Using info from recipe dictionary for %s", recipe_id)
        recipe_name = recipe_dict[recipe_id]["recipe_name"]
        recipe_internal_loc = recipe_dict[recipe_id]["recipe_fp"]

    # Or use the defaults
    else:
        logger.debug(
            "Using default name and filepath for recipe %s", recipe_id
        )
        recipe_name = f"recipe_{recipe_id}.yml"
        recipe_internal_loc = recipe_name

    return recipe_name, recipe_internal_loc


def fetch_recipe(recipe_id, recipe_dict_fp, output_filepath):
    """
    Fetch a recipe from ESMValTool and copy it to the output filepath.

    Parameters
    ----------
    recipe_id : str
        The short identifier of the recipe to retrieve,
        as written in the `flow.cylc` file.
    recipe_dict_fp : str
        The filepath of the YAML file containing the name and location
        within esmvaltool.recipes of the recipe to be fetched.
    output_filepath: str
        The full path to the where the ESMValTool recipe will be written.
    """
    # Find the full name and location within ESMValTool
    recipe_name, recipe_internal_loc = retrieve_name_and_fp(
        recipe_id, recipe_dict_fp
    )

    # Build the command to fetch and move the recipe
    command = f"""
    esmvaltool recipes get {recipe_internal_loc}
    mv {recipe_name} {output_filepath}
    """

    # Run the command
    logging.info("Running command: %s", command)
    subprocess.run(command, shell=True)
