#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

"""
Script to produce an HTML file using a jinja2 template file.
"""

import configparser
from jinja2 import Environment, FileSystemLoader
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def load_template(template_path):
    """Load and return jinja2 template from the given path.

    Args:
        template_path (Path): Path to jinja2 template file

    Returns:
        Template: Jinja2 template
    """
    logging.info(f"Reading template file {template_path}")
    env = Environment(loader=FileSystemLoader(template_path.parent))
    return env.get_template(template_path.name)


def load_data(data_path):
    """Routine to load data required for template

    Currently just reading data from a config/ini style file, could
    be set up to read a YAML or XML file?
    """
    logging.info(f"Reading template data from {data_path}")
    if data_path.suffix == ".conf":
        # Reading config/ini style input
        config = configparser.ConfigParser()
        config.read(data_path)
        template_data = dict(**config["env"])
    else:
        logging.error("This routine can only handle config files at present")
    logging.info(f"Template data acquired is {template_data}")
    return template_data


def produce_webpage(template_path, html_path, data_path):
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
