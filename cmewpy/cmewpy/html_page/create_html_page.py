#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

"""
Script to produce an HTML file using a jinja2 template file.
"""

from jinja2 import Environment, FileSystemLoader, Template
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def load_template(template_path: Path) -> Template:
    """Load and return jinja2 template from the given path.

    Args:
        template_path (Path): Path to jinja2 template file

    Returns:
        Template: Jinja2 template
    """
    logging.info(f"Reading template file {template_path}")
    env = Environment(loader=FileSystemLoader(template_path.parent))
    return env.get_template(template_path.name)


def load_data(data_path: Path | None) -> dict:
    """Routine to load data required for template

    Currently just reading environment variables to match existing API, could
    be set up to read a YAML, XML or config file?
    """
    logging.info("Using predefined environment variables to create data")
    logging.info(f"ASSESSMENT_TITLE = {os.environ['ASSESSMENT_TITLE']}")
    logging.info(f"DATASETS = {os.environ['DATASETS'}")
    logging.info(f"START_YEAR = {os.environ['START_YEAR']} ")
    logging.info(f"NUMBER_OF_YEARS = {os.environ['NUMBER_OF_YEARS']}")
    return {
        "title": os.environ["ASSESSMENT_TITLE"],
        "datasets": os.environ["DATASETS"],
        "start_year": os.environ["START_YEAR"],
        "number_of_years": os.environ["NUMBER_OF_YEARS"],
    }


def produce_html(
    template_path: Path, html_path: Path, data_path: Path | None
) -> None:
    """Main routine to produce html page.

    Args:
        template_path (Path): Path to jinja2 template file
        html_path (Path): Path to html output file

    Keyword Args:
        data_path (Path): Path to input file containing template variables
                          (Default: None)

    Returns:
        None
    """
    template = load_template(template_path)
    data = load_data(data_path)

    logging.info("Rendering jinja2 template with data")
    result = template.render(**data)

    logging.info(f"Creating HTML file: {html_path}")
    with open(html_path, "w") as fout:
        fout.writelines(result)
