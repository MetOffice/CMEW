#!/usr/bin/env python
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from esmvalcore.experimental.recipe import Recipe


def parse_variables_from_recipe(recipe_path):
    """Retrieve variables from ESMValTool recipe.

    * Read the ESMValTool recipe YAML file from the provided ``recipe_path``
    * For each diagnostic defined in the recipe, extract the variables required
      for that diagnostic
    * For each variable, extract the mip table name
    * Output a newline-separated list of variables, with each line formatted
      as ``<mip>/<variable>``

    Recipe file snippet::

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

    Will be formatted as::

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
    diagnostics = recipe.data["diagnostics"]
    formatted_variables = []
    for diagnostic in diagnostics:
        variables = diagnostics[diagnostic]["variables"]
        for variable in variables:
            mip = variables[variable]["mip"]
            formatted_variable = f"{mip}/{variable}"
            if formatted_variable not in formatted_variables:
                formatted_variables.append(formatted_variable)
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
    with open(target_path, "w") as target_file:
        target_file.write(variables_str)


def main():
    recipe_path = os.environ["RECIPE_PATH"]
    variables = parse_variables_from_recipe(recipe_path)
    write_variables(variables, os.environ["VARIABLES_PATH"])


if __name__ == "__main__":
    main()
