#!/usr/bin/env python
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from esmvalcore.experimental.recipe import Recipe


def parse_variables_from_recipe(recipe_path):
    """Retrieve variables from ESMValTool recipe.

    Parameters
    ----------
    recipe_path : str
        Location of the ESMValTool recipe file in the installed workflow.

    Returns
    -------
    str
        The variables from the ESMValTool recipe, separated by newlines.
    """
    recipe = Recipe(recipe_path)
    diagnostics = recipe.data["diagnostics"]
    variables = []
    for diagnostic in diagnostics:
        variables_dict = diagnostics[diagnostic]["variables"]
        for variable in variables_dict:
            mip = variables_dict[variable]["mip"]
            variable_str = mip + "/" + variable
            if variable_str not in variables:
                variables.append(variable_str)
    variables_str = "\n".join(variables)
    return variables_str


def write_variables(variables, target_path):
    """Write a string of variables to a text file in the installed workflow.

    Parameters
    ----------
    variables : str
        Formatted string of variables to be written to file.

    target_path : str
        Location to write the variables file.
    """
    with open(target_path, "w+") as target_file:
        target_file.write(variables)


def main():
    recipe_path = os.path.join(
        os.environ["RECIPE_PATH"], os.environ["RECIPE_NAME"]
    )
    variables = parse_variables_from_recipe(recipe_path)
    write_variables(variables, os.environ["VARIABLES_PATH"])


if __name__ == "__main__":
    main()
