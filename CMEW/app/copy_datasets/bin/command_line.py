# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from add_datasets_to_share import add_datasets_to_share


def parse_args_for_add_datasets_to_share(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_add_datasets_to_share`.

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
            "Copy the datasets defined in namelist files
            into YAML files."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source_dir",
        help="The directory containing the namelist files of datasets.",
    )
    parser.add_argument(
        "--target_dir",
        help="The directory into which to write the YAML files.",
    )
    parser.add_argument(
        "--start_year", help="The first year to extract for each dataset."
    )
    parser.add_argument(
        "--number_of_years",
        help="The number of years to extract for each dataset.",
    )
    parser.add_argument(
        "--institute", help="The institution ID to add to the datasets."
    )
    return parser.parse_args(arguments)


def main_for_add_datasets_to_share(arguments=None):
    """
    Copy dataset information from configuration to the share directory.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_add_datasets_to_share(arguments)

    # Run the code.
    print("Copying dataset information to the share directory.")
    print(f"Directory containing nl files: {args.source_dir}")
    print(f"Directory to output dataset lists: {args.target_dir}")
    print(f"Start year: {args.start_year}")
    print(f"Number of years: {args.number_of_years}")
    print(f"Institution ID: {args.institute}")
    add_datasets_to_share(
        args.source_dir,
        args.target_dir,
        args.start_year,
        args.number_of_years,
        args.institute,
    )
