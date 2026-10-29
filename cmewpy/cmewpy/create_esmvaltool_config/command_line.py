# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse

from cmewpy.create_esmvaltool_config.create_esmvaltool_config import (
    create_esmvaltool_config,
)


def parse_args_for_create_esmvaltool_config(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_create_esmvaltool_config`.

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
        description="Setup the configuration for ESMValTool.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--site_config_defaults_filepath",
        help=(
            "The full path to the YAML file containing the "
            "site-specific configuration for ESMValTool."
        ),
    )
    parser.add_argument(
        "--user_config_defaults_filepath",
        help=(
            "The full path to the YAML file containing the "
            "user-specific configuration for ESMValTool."
        ),
    )
    parser.add_argument(
        "--site_local_data_key",
        help=(
            "The site-specific fourth-level key "
            "in the ESMValTool site configuration file, "
            "occurring between 'data' and 'rootpath'."
        ),
    )
    parser.add_argument(
        "--cmew_data_for_esmval_dir",
        help=(
            "The full path to the directory where data "
            "processed with CMEW will be stored."
        ),
    )
    parser.add_argument(
        "--max_parallel_tasks",
        help="A parallelisation option to feed to ESMValTool.",
    )
    parser.add_argument(
        "--output_dir",
        help=(
            "The full path to the directory "
            "for ESMValTool to write its output."
        ),
    )
    parser.add_argument(
        "--site_config_output_path",
        help=(
            "The full path to the file where the "
            "site config file for ESMValTool will be written."
        ),
    )
    parser.add_argument(
        "--user_config_output_path",
        help=(
            "The full path to the file where the "
            "user config file for ESMValTool will be written."
        ),
    )

    return parser.parse_args(arguments)


def main_for_create_esmvaltool_config(arguments=None):
    """
    Setup the configuration for ESMValTool.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_create_esmvaltool_config(arguments)

    # Run the code.
    print(
        f"site_config_defaults_filepath: {args.site_config_defaults_filepath}"
    )
    print(
        f"user_config_defaults_filepath: {args.user_config_defaults_filepath}"
    )
    print(f"cmew_data_for_esmval_dir: {args.cmew_data_for_esmval_dir}")
    print(f"site_local_data_key: {args.site_local_data_key}")
    print(f"max_parallel_tasks: {args.max_parallel_tasks}")
    print(f"output_dir: {args.output_dir}")
    print(f"site_config_output_path: {args.site_config_output_path}")
    print(f"user_config_output_path: {args.user_config_output_path}")
    create_esmvaltool_config(
        args.site_config_defaults_filepath,
        args.user_config_defaults_filepath,
        args.site_local_data_key,
        args.cmew_data_for_esmval_dir,
        args.max_parallel_tasks,
        args.output_dir,
        args.site_config_output_path,
        args.user_config_output_path,
    )
