# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from create_variables_file import create_variables_file


def parse_args_for_create_variables_file(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_create_variables_file`.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.

    Returns
    -------
    :class:`argparse.Namespace`
        The names and values of the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create a request to standardise model data with CDDS.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--vars_files_list_dir",
        help=(
            "The path to the directory containing "
            "the lists of variables from each recipe."
        ),
    )
    parser.add_argument(
        "--stream_config_fp",
        help=(
            "The full path to the file where the "
            "data streams containing each variable are written."
        ),
    )
    parser.add_argument(
        "--output_filepath",
        help=(
            "The full path to the file where the "
            "variables from the ESMValTool recipe will be written."
        ),
    )
    return parser.parse_args(arguments)


def main_for_create_variables_file(arguments=None):
    """
    Generates the variables.txt file from the ESMValTool recipes.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_create_variables_file(arguments)

    # Run the code.
    print(f"variable_list_file: {args.vars_files_list_dir}"),
    print(f"stream_config_fp: {args.stream_config_fp}"),
    print(f"output_filepath: {args.output_filepath}"),
    create_variables_file(
        args.vars_files_list_dir,
        args.stream_config_fp,
        args.output_filepath,
    )
