#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Scrape model_run suite_ids from an ini-style file.
"""


def extract_suite_ids(content):
    """
    Lists the suite IDs of model runs from the content of an ini-style file.

    Checks the whole file for lines starting "suite_id".

    Parameters
    ----------
    content: list of strings
        The lines of the ini-style file

    Returns
    -------
    list
        The list of suite_ids (unquoted).
    """
    # Initialise overall list
    suite_ids = []

    # Read each line in turn
    for line in content:

        # Look for relevant lines
        if line.startswith("suite_id"):

            # Take the value of the suite ID
            suite_id = line.split("=")[1]

            # Add to the list, unquoted
            suite_ids.append(suite_id.strip().replace('"', ""))

    return suite_ids


def list_datasets(fp):
    """
    Obtain a string listing the suite_ids from an ini-style file.

    Saves the unquoted value of every line starting "suite_id"
    into a comma-and-space separated string.

    Parameters
    ----------
    fp: str
        The file path to the ini-style file.

    Returns
    -------
    str
        The list of suite_ids, in a comma separated string.
    """
    # Read the file
    with open(fp, "r") as f:
        content = f.readlines()

    # Get a list of suite IDs
    datasets = extract_suite_ids(content)

    # Write the list as a comma separated string
    datasets_string = ", ".join(datasets)

    return datasets_string
