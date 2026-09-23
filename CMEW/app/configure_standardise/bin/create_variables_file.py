#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Create a variables file to standardise model data with CDDS.
"""
import os
import sys
import logging
from config_configure_standardise import streams_dict


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


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
            logger.debug("Reading variables from %s", filename)
            with open(os.path.join(directory, filename), "r") as file:
                recipe_vars = file.read().splitlines()
                for var in recipe_vars:
                    if var not in variables:
                        logger.debug("Found variable %s", var)
                        variables.append(var)
    return variables


def add_stream_to_variables(variables, streams_dict=streams_dict):
    """Add stream information to a list of variables.

    Parameters
    ----------
    variables : list[str]
        List of variables in the format "MIP_table/variable_name"
    streams_dict : dict
        A dictionary containing information about data streams.

    Returns
    -------
    list[str]
        List of variables in the format "MIP_table/variable_name:stream"
    """
    # Using a second dictionary to avoid looping
    var_to_stream = {
        var: stream
        for stream, var_list in streams_dict.items()
        for var in var_list
    }

    # Listing the input variables together with their stream
    streamed_variables = [
        f"{var}:{var_to_stream.get(var)}" for var in variables
    ]
    logger.debug("Variables with streams:\n%s", streamed_variables)

    return streamed_variables


def write_variables(variables, output_filepath):
    """Write a string of variables to a text file in the installed workflow.

    Parameters
    ----------
    variables : list[str]
        List of variables to be written to file.

    output_filepath : str
        Location to write the variables file.
    """
    variables_str = "\n".join(variables) + "\n"
    logger.debug("Writing variables:\n%s", variables_str)

    with open(output_filepath, "w") as target_file:
        target_file.write(variables_str)


def create_variables_file(vars_files_list_dir, output_filepath):
    """Create a variables file to standardise model data with CDDS."""
    variables = combine_variable_lists(vars_files_list_dir)
    streamed_variables = add_stream_to_variables(variables)
    logger.info("Writing variables file to %s", output_filepath)
    write_variables(streamed_variables, output_filepath)
