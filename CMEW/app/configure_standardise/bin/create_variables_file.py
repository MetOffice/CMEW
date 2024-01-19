#!/usr/bin/env python
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from pathlib import Path


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
    with open(recipe_path) as source_file:
        variables = source_file.read()
    return variables


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
    mock_path = Path(__file__).parent.parent / "mock_data" / "variables.txt"
    variables = parse_variables_from_recipe(mock_path)
    write_variables(variables, os.environ["VARIABLES_PATH"])


if __name__ == "__main__":
    main()
