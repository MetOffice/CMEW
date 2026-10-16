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
            print(f"[scrape_ini.py] Found line: {line}")

            # Take the value of the suite ID
            suite_id = line.split("=")[1]

            # Add to the list, unquoted
            suite_ids.append(suite_id.strip().replace('"', ""))

    print(f"[scrape_ini.py] Suite IDs found: {suite_ids}")
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

    print(f"[scrape_ini.py] Datasets found: {datasets_string}")
    return datasets_string


def retrieve_value(fp, indicator, key):
    """
    Return the value of a key from the indicated section of an ini-style file.
    """
    # Provide a default in case things go wrong
    value = None

    # Read the file
    with open(fp, "r") as f:
        content = f.readlines()

    # Iterate over the lines
    for index, line in enumerate(content):

        # Look for relevant sections
        line_to_find = f"[namelist:model_runs({indicator})]"
        if line.startswith(line_to_find):

            # Look for next line starting with the key
            next_index = index + 1
            for next_line in content[next_index:]:
                if next_line.strip().startswith(key):
                    # Split the line and take the second part without quotes
                    value = next_line.split("=")[1].strip().replace('"', "")

                    # Break the inner loop
                    break

    print(f"[scrape_ini.py] Retrieved value: {value}")
    return value


def find_ref(fp):
    """Return the reference suite ID"""
    ref_suite_id = retrieve_value(fp, "reference", "suite_id")
    print(f"[scrape_ini.py] Ref suite ID: {ref_suite_id}")
    return ref_suite_id


def find_eval(fp):
    """Return the evaluation suite ID"""
    eval_suite_id = retrieve_value(fp, "experiment", "suite_id")
    print(f"[scrape_ini.py] Eval suite ID: {eval_suite_id}")
    return eval_suite_id


def find_ref_label(fp):
    """Return the reference label for plots"""
    ref_label = retrieve_value(fp, "reference", "label_for_plots")
    print(f"[scrape_ini.py] Ref label: {ref_label}")
    return ref_label


def find_eval_label(fp):
    """Return the evaluation label for plots"""
    eval_label = retrieve_value(fp, "experiment", "label_for_plots")
    print(f"[scrape_ini.py] Eval label: {eval_label}")
    return eval_label
