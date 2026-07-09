# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from get_variables_from_recipe import get_variables_from_recipe


def parse_args(arguments):
    """
    Return the names and values of the command line arguments for :func:`main`.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.

    Returns
    -------
    :class:`argparse.Namespace`
        The names of the command line arguments and their validated
        values.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve variables from an ESMValTool recipe.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--recipe_path",
        help="The name of the variable to download.",
    )
    parser.add_argument(
        "--output_filepath",
        help=(
            "The full path to the file where the "
            "variables data will be written."
        ),
    )

    return parser.parse_args(arguments)


def main(arguments=None):
    args = parse_args(arguments)
    get_variables_from_recipe(args.recipe_path, args.output_filepath)
