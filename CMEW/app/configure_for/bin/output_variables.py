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

    This function will first look to see if the variable's "short_name"
    key is present and use it if so or return a higher level of key if not.

    * Read the ESMValTool recipe YAML file from the provided ``recipe_path``
    * For each diagnostic defined in the recipe, extract the variables required
      for that diagnostic
    * For each variable, extract the mip table name
    * Output a newline-separated list of variables, with each line formatted
      as ``<mip>/<variable>``

    Recipe file snippet, format 1::

        diagnostics:
          <diagnostic_1>:
            variables:
              other_key_name_1:
                short_name: <variable_1a>:
                mip: <mip_1a>
              other_key_name_2:
                short_name: <variable_1b>:
                mip: <mip_1b>
          <diagnostic_2>:
            variables:
              other_key_name_3:
                short_name: <variable_2a>:
                mip: <mip_2a>
              other_key_name_4:
                short_name: <variable_2b>:
                mip: <mip_2b>

    Will be formatted as::

        <mip_1a>/<variable_1a>
        <mip_1b>/<variable_1b>
        <mip_2a>/<variable_2a>
        <mip_2b>/<variable_2b>

    Recipe file snippet, format 2::

        diagnostics:
          <diagnostic_1>:
            variables:
              <variable_1a>:
                mip: <mip_1a>
              <variable_1b>:
                mip: <mip_1b>
          <diagnostic_2>:
            variables:
              <variable_2a>:
                mip: <mip_2a>
              <variable_2b>:
                mip: <mip_2b>

    Will also be formatted as::

        <mip_1a>/<variable_1a>
        <mip_1b>/<variable_1b>
        <mip_2a>/<variable_2a>
        <mip_2b>/<variable_2b>

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
        for variable, variable_items in variables.items():
            log_text = "key"
            if "short_name" in variable_items:
                log_text = "short name"
                variable = variable_items["short_name"]
            logger.debug(f"Using {log_text} {variable}")

            # Look up the mip key which is, so far, always present
            mip = variable_items["mip"]

            # Construct the string expected by CDDS
            formatted_variable = f"{mip}/{variable}"

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
