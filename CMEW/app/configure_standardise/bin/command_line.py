# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from create_variables_file import create_variables_file
from create_request_file import create_request_file


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
        description=(
            "Create a variables file to standardise model data with CDDS."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--vars_files_list_dir",
        help=(
            "The full path to the directory containing "
            "the lists of variables from each recipe."
        ),
    )
    parser.add_argument(
        "--stream_config_fp",
        help=(
            "The full path to the file containing "
            "the data streams for each variable."
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
    Create a variables file to standardise model data with CDDS.

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


def parse_args_for_create_request_file(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_create_request_file`.

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
        "--dataset",
        help="The model run to be extracted from MASS and processed.",
    )
    parser.add_argument(
        "--output_filepath",
        help=(
            "The full path to the file where the "
            "variables from the ESMValTool recipe will be written."
        ),
    )
    parser.add_argument(
        "--defaults_path",
        help=(
            "The full path to the file where the "
            "default values for a CDDS request are written."
        ),
    )
    parser.add_argument(
        "--mip_table_dir",
        help="The MIP table to use from CDDS.",
    )
    parser.add_argument(
        "--model_runs_yml_fp",
        help=(
            "The full path to the YAML file "
            "containing details of the model runs."
        ),
    )
    parser.add_argument(
        "--root_proc_dir",
        help=(
            "The full path to the directory where CDDS "
            "should store data for the processing workflow."
        ),
    )
    parser.add_argument(
        "--root_data_dir",
        help=(
            "The full path to the directory where CDDS "
            "should store raw and standardised data."
        ),
    )
    parser.add_argument(
        "--variables_file",
        help=(
            "The full path to the file where the "
            "variables to be retrieved by CDDS are written."
        ),
    )
    parser.add_argument(
        "--raw_data_dir_mode",
        help=("Whether to save or reuse raw CDDS data files."),
    )
    return parser.parse_args(arguments)


def main_for_create_request_file(arguments=None):
    """
    Generate and write the request file for the current task environment.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_create_request_file(arguments)

    # Run the code.
    print(f"dataset: {args.dataset}"),
    print(f"output_filepath: {args.output_filepath}"),
    print(f"defaults_path: {args.defaults_path}"),
    print(f"mip_table_dir: {args.mip_table_dir}"),
    print(f"model_runs_yml_fp: {args.model_runs_yml_fp}"),
    print(f"root_proc_dir: {args.root_proc_dir}"),
    print(f"root_data_dir: {args.root_data_dir}"),
    print(f"variables_file: {args.variables_file}"),
    print(f"raw_data_dir_mode: {args.raw_data_dir_mode}"),
    create_request_file(
        args.dataset,
        args.output_filepath,
        args.defaults_path,
        args.mip_table_dir,
        args.model_runs_yml_fp,
        args.root_proc_dir,
        args.root_data_dir,
        args.variables_file,
        args.raw_data_dir_mode,
    )
