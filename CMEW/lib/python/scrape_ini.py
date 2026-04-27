#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Scrape model_run suite_ids from an ini-style file.
"""


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
    # Read the file
    with open(fp, "r") as f:
        content = f.readlines()

    # Initialize list
    datasets = []

    # Iterate over the lines
    for line in content:

        # Look for relevant sections
        if line.startswith("[namelist:model_runs"):

            # Look for next line starting "suite_id"
            next_index = content.index(line) + 1
            for next_line in content[next_index:]:
                if next_line.strip().startswith("suite_id"):
                    # Split the line and take the second part without quotes
                    dataset = next_line.split("=")[1].strip().replace('"', "")

                    # Add to list
                    datasets.append(dataset)

                    # Break the inner loop
                    break

    datasets_string = ", ".join(dataset for dataset in datasets)
    return datasets_string
