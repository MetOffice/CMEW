# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from get_variables_from_recipe import get_variables_from_recipe
from fetch_recipe import fetch_recipe
from update_recipe_file import update_recipe_file


def parse_args_for_get_variables_from_recipe(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_get_variables_from_recipe`.

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
        description="Retrieve variables from an ESMValTool recipe.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--recipe_path",
        help="The full path to the ESMValTool recipe.",
    )
    parser.add_argument(
        "--output_filepath",
        help=(
            "The full path to the file where the "
            "variables from the ESMValTool recipe will be written."
        ),
    )
    return parser.parse_args(arguments)


def main_for_get_variables_from_recipe(arguments=None):
    """
    Retrieve variables from an ESMValTool recipe.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_get_variables_from_recipe(arguments)

    # Run the code.
    print("Retrieving variables from recipe.")
    print(f"Recipe path: {args.recipe_path}")
    print(f"Output filepath: {args.output_filepath}")
    get_variables_from_recipe(args.recipe_path, args.output_filepath)


def parse_args_for_fetch_recipe(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_fetch_recipe`.

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
        description="Retrieve an ESMValTool recipe.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--recipe_id",
        help=(
            "The short identifier of the recipe to retrieve, "
            "as written in the `flow.cylc` file."
        ),
    )
    parser.add_argument(
        "--recipe_dict_fp",
        help=(
            "The filepath of the YAML file containing the "
            "name and location within esmvaltool.recipes "
            "of the recipe to be fetched."
        ),
    )
    parser.add_argument(
        "--output_filepath",
        help=(
            "The full path to the where the "
            "ESMValTool recipe will be written."
        ),
    )
    return parser.parse_args(arguments)


def main_for_fetch_recipe(arguments=None):
    """
    Retrieve an ESMValTool recipe.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_fetch_recipe(arguments)

    # Run the code.
    print("Fetching recipe.")
    print(f"Recipe ID: {args.recipe_id}")
    print(f"Recipe dict filepath: {args.recipe_dict_fp}")
    print(f"Output filepath: {args.output_filepath}")
    fetch_recipe(args.recipe_id, args.recipe_dict_fp, args.output_filepath)


def parse_args_for_update_recipe_file(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_update_recipe_file`.

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
        description="Update the datasets in an ESMValTool recipe.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--recipe_path",
        help="The full path to the ESMValTool recipe.",
    )
    parser.add_argument(
        "--model_runs_yml_fp",
        help=(
            "The full path to the YAML file "
            "containing details of the model runs."
        ),
    )
    parser.add_argument(
        "--cmip6_datasets_yml_fp",
        help=(
            "The full path to the YAML file "
            "containing details of the CMIP6 datasets to include."
        ),
    )
    parser.add_argument(
        "--recipe_id",
        help=("The parameter CYLC_TASK_PARAM_recipe"),
    )
    parser.add_argument(
        "--recipe_dict_fp",
        help=(
            "The full path to the YAML file containing the "
            "name and location within esmvaltool.recipes "
            "of the recipe to be amended"
        ),
    )
    return parser.parse_args(arguments)


def main_for_update_recipe_file(arguments=None):
    """
    Update the datasets in an ESMValTool recipe.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_update_recipe_file(arguments)

    # Run the code.
    print("Updating recipe file.")
    print(f"Recipe path: {args.recipe_path}")
    print(f"Model runs YAML path: {args.model_runs_yml_fp}")
    print(f"CMIP6 datasets YAML path: {args.cmip6_datasets_yml_fp}")
    print(f"Recipe ID: {args.recipe_id}")
    print(f"Recipe dict filepath: {args.recipe_dict_fp}")
    update_recipe_file(
        args.recipe_path,
        args.model_runs_yml_fp,
        args.cmip6_datasets_yml_fp,
        args.recipe_id,
        args.recipe_dict_fp,
    )
