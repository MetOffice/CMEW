#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Scrape model_run suite_ids from an ini-style file.
"""
import configparser
import sys

# Using config parser to error on duplicate keys or headings
config = configparser.ConfigParser()

class ConfigError(Exception):
    pass


def list_datasets(fp):
    """
    Obtain a string listing the suite_ids from an ini-style file.

    Uses hardcoded value "[namelist:model_runs" to identify a section
    and then adds the next "suite_id" to the string.

    Parameters
    ----------
    fp: str
        The file path to the ini-style file.

    Returns
    -------
    str
        The list of suite_ids, in a comma separated string.
    """
    # Should fail if there's a duplicate heading
    try:
        # Read the file
        config.read(fp)

    except configparser.Error:
        raise ConfigError("Error in the rose_suite.conf file")

    # Initialize list
    datasets = []

    # Iterate over the sections
    for section in config.sections():

        # Only look at model run sections
        if section.startswith("namelist:model_runs("):

            # Ensure section has suite ID:
            try:
                # Find the dataset by the key "suite_id"
                dataset = config[section]["suite_id"]

            except KeyError:
                raise ConfigError("Suite ID missing from rose_suite.conf")

            # Strip the quotes
            dataset = dataset.replace('"', "")

            # Add the dataset to the list
            datasets.append(dataset)

    datasets_string = ", ".join(datasets)
    return datasets_string
