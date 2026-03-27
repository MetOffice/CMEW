#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Scrape model_run suite_ids from an ini-style file.
"""
def list_datasets(fp):
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
            for next_line in content[content.index(line) + 1:]:
                if next_line.strip().startswith("suite_id"):
                    # Split the line on = and take the second part without quotes
                    dataset = next_line.split("=")[1].strip().replace('"', "")

                    # Add to list
                    datasets.append(dataset)

                    # Break the inner loop
                    break

    return datasets
