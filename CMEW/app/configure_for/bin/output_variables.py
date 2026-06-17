#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Outputs the variables from an ESMValTool recipe.
"""
import os
from esmvalcore.experimental.recipe import Recipe
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def parse_variables_from_recipe(recipe_path):
    """Retrieve variables from ESMValTool recipe.

    This function will first look to see if the variable's "short_name" key is present,
    and use it if so or return a higher level of key if not.

    Parameters
    ----------
    recipe_path : str
        Location of the ESMValTool recipe file.

    Returns
    -------
    list[str]
        List of variables from the ESMValTool recipe,
        formatted as ``<mip>/<variable>``.
    """
    recipe = Recipe(recipe_path)
    logger.debug("Loading recipe %s", recipe_path)
    diagnostics = recipe.data["diagnostics"]
    formatted_variables = []
    for diagnostic in diagnostics:
        variables = diagnostics[diagnostic]["variables"]
        logger.debug("Diagnostic % variables:\n%s", diagnostic, variables)
        for variable in variables:
            # See if the short_name key is present and use it if so
            if "short_name" in variables[variable]:
                var = variables[variable]["short_name"]
                logger.debug("Using short name %s", var)
            else:
                var = variable
                logger.debug("Using key %s", var)

            # Look up the mip key which is always present
            mip = variables[variable]["mip"]

            # Construct the string expected by CDDS
            formatted_variable = f"{mip}/{var}"

            # Add only if not already present
            if formatted_variable not in formatted_variables:
                formatted_variables.append(formatted_variable)
                logger.debug("Adding variable %s", formatted_variable)
    return formatted_variables


def write_variables(variables, target_path):
    """Write a string of variables to a text file in the installed workflow.

    Parameters
    ----------
    variables : list[str]
        List of variables to be written to file.

    target_path : str
        Location to write the variables file.
    """
    variables_str = "\n".join(variables) + "\n"
    logger.debug("Writing variables:\n%s", variables_str)
    with open(target_path, "w") as target_file:
        target_file.write(variables_str)


def main():
    recipe_path = os.environ["RECIPE_PATH"]
    logger.info("Reading variables from %s", recipe_path)
    variables = parse_variables_from_recipe(recipe_path)
    variables_path = os.environ["RECIPE_VARIABLES_PATH"]
    logger.info("Writing variables to %s", variables_path)
    write_variables(variables, variables_path)


if __name__ == "__main__":
    main()
