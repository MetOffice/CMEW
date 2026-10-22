#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Create a variables file to standardise model data with CDDS.
"""
import os
import sys
import logging
from cmewpy.configure_standardise.config_configure_standardise import (
    streams_dict,
)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def retrieve_variables_files_contents(directory):
    """
    Return the contents of all variables files in a directory.

    Variables files are files ending with "_variables.txt".

    Parameters
    ----------
    directory : str
        The full path to the directory containing variables files.

    Returns
    -------
    list of list
       The contents of all variables files in the directory.
    """
    variables_files_contents = []
    for filename in os.listdir(directory):
        if filename.endswith("_variables.txt"):
            logger.debug("Reading variables from %s", filename)
            with open(os.path.join(directory, filename), "r") as file_handle:
                variables_files_contents.append(
                    [line.strip() for line in file_handle]
                )
    return variables_files_contents


def determine_unique_variables(variables):
    """
    Return the unique variables from the variables.

    Parameters
    ----------
    variables: list of list
        The variables, which may or may not contain duplicates.

    Returns
    -------
    list of str
        The unique variables.

    """
    unique_variables = []
    for variable_list in variables:
        for variable in variable_list:
            if variable not in unique_variables:
                logger.debug("Found variable %s", variable)
                unique_variables.append(variable)
    return unique_variables


def add_stream_to_variables(variables, streams_dict=streams_dict):
    """Add stream information to a list of variables.

    Parameters
    ----------
    variables : list of str
        List of variables in the format "MIP_table/variable_name"
    streams_dict : dict
        A dictionary containing information about data streams.

    Returns
    -------
    list of str
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
    variables : list of str
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
    variables = retrieve_variables_files_contents(vars_files_list_dir)
    unique_variables = determine_unique_variables(variables)
    streamed_variables = add_stream_to_variables(unique_variables)
    logger.info("Writing variables file to %s", output_filepath)
    write_variables(streamed_variables, output_filepath)
