#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os


def combine_variable_lists(directory):
    """Combine all variables list files from a directory.

    Looks for files ending with "_variables.txt" in the specified directory,
    reads the lines of each file, deletes any duplicates and
    then returns a single list of unique lines.

    Parameters
    ----------
    directory : str
        Path to the directory containing variables list files.
    Returns
    -------
    list[str]
        A combined list of unique variables from all files in the directory.
    """
    variables = []
    for filename in os.listdir(directory):
        if filename.endswith("_variables.txt"):
            with open(os.path.join(directory, filename), "r") as file:
                recipe_vars = file.read().splitlines()
                for var in recipe_vars:
                    if var not in variables:
                        variables.append(var)
    return variables


def manually_amend_variables(variables):
    """Make CMEW-specific amendments to a list of variables.

    Parameters
    ----------
    variables : list[str]
        List of variables to be amended.

    Returns
    -------
    list[str]
        Amended list of variables.
    """
    # Remove fixed variables that don't need retrieving from MASS
    vars_to_remove = ["fx/areacello"]
    for var in variables:
        if var in vars_to_remove:
            variables.remove(var)

    # Change OImon to SImon
    for i, var in enumerate(variables):
        if var.startswith("OImon/"):
            variables[i] = var.replace("OImon/", "SImon/")

    # Add stream information here instead of using CDDS's stream_mappings
    stream_dict = {
        "apm": [
            "Amon/hfls",
            "Amon/hfss",
            "Amon/rlds",
            "Amon/rlut",
            "Amon/rlutcs",
            "Amon/rsds",
            "Amon/rsdt",
            "Amon/rsut",
            "Amon/rsutcs",
            "Emon/rls",
            "Emon/rss",
            "Amon/tas",  # This is new, might not be right
            "Amon/pr",  # This is new, might not be right
        ],
        "inm": [
            "SImon/sic",  # Also new, from guessing streams with CDDS
        ],
    }
    streamed_variables = []
    for var in variables:
        for stream, var_list in stream_dict.items():
            if var in var_list:
                streamed_var = f"{var}:{stream}"
                streamed_variables.append(streamed_var)
                break

    return streamed_variables


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
    variables = combine_variable_lists(os.environ["VARIABLES_LIST_DIR"])
    variables = manually_amend_variables(variables)
    write_variables(variables, os.environ["VARIABLES_PATH"])


if __name__ == "__main__":
    main()
