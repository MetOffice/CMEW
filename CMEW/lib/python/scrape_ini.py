#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Scrape model_run suite_ids from an ini-style file.
"""


def check_no_duplicate_sections(content):
    """
    Raise an exception if there are duplicate section headers.

    Parameters
    ----------
    content: list of strings
        The lines of the ini-style file

    """
    # List headers in content
    list_headers = []
    for line in content:

        # Look for section headers
        if line.startswith("["):
            list_headers.append(line)

    # Use a set to remove duplicates
    if len(list_headers) != len(set(list_headers)):
        raise ValueError("Duplicate sections in rose_suite.conf file")


def extract_suite_ids(content):
    """
    Lists the suite IDs of model runs from the content of an ini-style file.

    Identifies a relevant section as one starting "[namelist:model_runs".
    Checks that section for lines starting "suite_id", and makes a list of these values.
    Ensures there is exactly one suite ID per relevant section.
    Returns a list of the suite IDs from the relevant sections.

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
    for index, line in enumerate(content):

        # Look for relevant section
        if line.startswith("[namelist:model_runs"):

            # Initialise list for that section
            suites_in_section = []

            # Read from the next line onwards
            for subsequent_line in content[index+1:]:

                # Look for the suite ID
                if subsequent_line.startswith("suite_id"):

                    # Take the value of the suite ID
                    suite_id = subsequent_line.split("=")[1]

                    # Add to the list for the section, unquoted
                    suites_in_section.append(suite_id.strip().replace('"', ""))

                # Stop reading if a new section starts
                elif subsequent_line.startswith("["):
                    break

            # Raise an error if there is not exactly one suite ID
            if not len(suites_in_section) == 1:
                raise ValueError(f"Section {line} did not contain exactly one suite_id")

            # Add that section's suite ID to the overall list
            else:
                suite_ids.append(suites_in_section[0])  # [0] as it is from a list

    return suite_ids


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

    # Check section headers are unique
    check_no_duplicate_sections(content)

    # Get a list of suite IDs
    datasets = extract_suite_ids(content)

    # Write the list as a comma separated string
    datasets_string = ", ".join(datasets)

    return datasets_string
