#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from pathlib import Path
import yaml


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
    for filename in sorted(os.listdir(directory)):  # sorted only to unit test
        if filename.endswith("_variables.txt"):
            with open(os.path.join(directory, filename), "r") as file:
                recipe_vars = file.read().splitlines()
                for var in recipe_vars:
                    if var not in variables:
                        variables.append(var)
    return variables


def load_stream_dict():
    """
    Loads stream information from the ../etc/streams.yml file.

    Returns
    -------
    dict
        A mapping of pre-defined streams to their associated variables
    """
    # Set path to stream mappings
    streams_config = Path(__file__).parent.parent / "etc" / "streams.yml"

    # Read the stream mappings
    with open(streams_config, "r") as f:
        config = yaml.safe_load(f)

    # Return the whole dictionary
    return config


def add_stream_to_variables(variables):
    """Add stream information to a list of variables.

    Parameters
    ----------
    variables : list[str]
        List of variables in the format "MIP_table/variable_name"

    Returns
    -------
    list[str]
        List of variables in the format "MIP_table/variable_name:stream"
    """
    stream_dict = load_stream_dict()

    # Using a second dictionary to avoid looping
    var_to_stream = {
        var: stream
        for stream, var_list in stream_dict.items()
        for var in var_list
    }

    # Listing the input variables together with their stream
    streamed_variables = [
        f"{var}:{var_to_stream.get(var)}" for var in variables
    ]

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
    streamed_variables = add_stream_to_variables(variables)
    write_variables(streamed_variables, os.environ["VARIABLES_PATH"])


if __name__ == "__main__":
    main()
