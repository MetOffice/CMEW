# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import argparse
from pathlib import Path
from cmewpy.html_page.create_html_page import produce_html_page


def parse_args_for_create_html_page(arguments):
    """
    Return the names and values of the command line arguments for
    :func:`main_for_create_html_page`.

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
            "Produce an HTML page using a jinja2 template."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--template", type=Path, help="Jinja2 template file.",
    )
    parser.add_argument(
        "--html-page", type=Path, help="File to write output to.",
    )
    parser.add_argument(
        "-d", "--data", type=Path, default=None, help="Data file with inputs.",
    )
    return parser.parse_args(arguments)


def main_for_create_html_page(arguments=None):
    """
    Produce an HTML web page using the defined inputs and jinja2

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    # Parse the arguments.
    args = parse_args_for_create_html_page(arguments)

    # Run the code.
    print("Copying the datasets defined in namelist files into YAML files.")
    print(f"Template file for jinja2: {args.template}")
    print(f"Output HTML path: {args.html_page}")
    print(f"Data Path: {args.data}")
    produce_html_page(
        args.template,
        args.html_page,
        args.data,
    )

