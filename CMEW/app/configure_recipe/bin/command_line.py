# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse

from configure_recipe import configure_recipe


def parse_args_for_configure_recipe(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_configure_recipe`.

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
        description="Retrieve environment variables for ESMValTool config.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--cmew_data_for_esmval_dir",
        help="The full path to the directory where data "
        "processed with CMEW will be stored.",
    )
    parser.add_argument(
        "--dev_config_path",
        help=(
            "The full path to the file where the "
            "developer config file for ESMValTool will be written."
        ),
    )
    parser.add_argument(
        "--drs_cmip6",
        help=("The DRS for CMIP6."),
    )
    parser.add_argument(
        "--drs_obs4mips",
        help=("The DRS for obs4MIPS."),
    )
    parser.add_argument(
        "--max_parallel_tasks",
        help=("A parallelisation option to feed to ESMValTool."),
    )
    parser.add_argument(
        "--mip_table_dir",
        help=("The MIP table to use from CDDS."),
    )
    parser.add_argument(
        "--output_dir",
        help=("The path to the directory for ESMValTool to write its output."),
    )
    parser.add_argument(
        "--rootpath_cmip6",
        help=("The rootpath for CMIP6."),
    )
    parser.add_argument(
        "--rootpath_obs4mips",
        help=("The rootpath for obs4MIPS."),
    )
    parser.add_argument(
        "--user_config_path",
        help=(
            "The full path to the file where the "
            "user config file for ESMValTool will be written."
        ),
    )

    return parser.parse_args(arguments)


def main_for_configure_recipe(arguments=None):
    """
    Retrieve variables from an ESMValTool recipe.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_configure_recipe(arguments)

    # Run the code.
    print(f"cmew_data_for_esmval_dir: {args.cmew_data_for_esmval_dir}")
    print(f"dev_config_path: {args.dev_config_path}")
    print(f"drs_cmip6: {args.drs_cmip6}")
    print(f"drs_obs4mips: {args.drs_obs4mips}")
    print(f"max_parallel_tasks: {args.max_parallel_tasks}")
    print(f"mip_table_dir: {args.mip_table_dir}")
    print(f"output_dir: {args.output_dir}")
    print(f"rootpath_cmip6: {args.rootpath_cmip6}")
    print(f"rootpath_obs4mips: {args.rootpath_obs4mips}")
    print(f"user_config_path: {args.user_config_path}")
    configure_recipe(
        args.cmew_data_for_esmval_dir,
        args.dev_config_path,
        args.drs_cmip6,
        args.drs_obs4mips,
        args.max_parallel_tasks,
        args.mip_table_dir,
        args.output_dir,
        args.rootpath_cmip6,
        args.rootpath_obs4mips,
        args.user_config_path,
    )
