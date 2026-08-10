#!/usr/bin/env python
# (C) Crown Copyright 2022-2025, Met Office.
# The LICENSE.md file contains full licensing details.

"""
Script to produce an HTML file using a jinja2 template file.
"""

import argparse
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path


def load_template(template_path: Path) -> jinja2.environment.Template:
    """Load and return jinja2 template from the given path.

    Args:
        template_path (Path): Path to jinja2 template file

    Returns:
        jinja2.environment.Template: Jinja2 template
    """
    env = Environment(loader=FileSystemLoader(template_path.parent))
    return env.get_template(template_path.name)


def load_data(data_path: Path | None) -> dict:
    """Routine to load data required for template

    Currently just reading environment variables to match existing API, could
    be set up to read a YAML, XML or config file?
    """
    return {
        "title": os.environ["ASSESSMENT_TITLE"],
        "ref_suite_id": os.environ["REF_SUITE_ID"],
        "exp_suite_id": os.environ["SUITE_ID"],
        "start_date": os.environ["START_DATE"],
        "end_date": os.environ["END_DATE"],
    }


def produce_html(template_path: Path, html_path: Path, data_path: Path | None) -> None:
    """Main routine to produce html page.

    Args:
        template_path (Path): Path to jinja2 template file
        html_path (Path): Path to html output file

    Keyword Args:
        data_path (Path): Path to input file containing template variables (Default: None)

    Returns:
        None
    """
    template = load_template(template_path)
    data = load_data(data_path)

    result = template.render(**data)

    with open(html_path, "w") as fout:
        fout.writelines(result)


def read_args() -> argparse.Namespace:
    """Reading command line inputs.
    """

    # Create argument parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Add arguments
    parser.add_argument(
        "template", type=Path, dict(help="Jinja2 template file.")
    )
    parser.add_argument(
        "html_page", type=Path, dict(help="File to write output to.")
    )
    parser.add_argument(
        "-d", "--data", type=Path, default=None, dict(help="Data file.")
    )

    # Return parsed arguments
    return parser.parse_args()


def main():
    args = read_args()
    produce_html(args.template, args.html, args.data)


if __name__ == "__main__":
    main()
