#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Process and copy the dataset namelist files to a shared directory.

Namelist files are created by rose from the sections in
CMEW/app/add_datasets/rose-app.conf. These may be edited in the GUI.
This application reads the namelist files,
converts the contents to a dictionary of datasets and their facets,
then writes those dictionaries to YAML files in the share directory.
"""
import os
from common import write_dict_to_yaml


def extract_sections_from_naml(naml_fp):
    """
    Read sections from a namelist file and return them as a list of strings.

    Parameters
    ----------
    naml_fp: str
        The file path to the namelist file containing the datasets.

    Returns
    -------
    datatsets: list of str
        A list of strings, each containing the content of a section in the
        namelist file minus the headers and separating characters.
    """

    # Read the namelist file
    with open(naml_fp, "r") as file:
        content = file.read()

    # Namelist files are separated by a line containing only "/"
    datasets = content.split("\n/\n")

    # Read the line containing the header for the first dataset's section
    first_dataset = datasets[0]
    first_line = first_dataset.split("\n")[0]
    name = first_line.replace("&", "")  # This could be returned if needed

    # Initialise a list to hold the extracted datasets
    extracted_datasets = []

    for dataset in datasets:
        if dataset:  # There is an empty dataset at the end
            # Replace newlines with just commas
            dataset = dataset.replace(",\n", ",")

            # Remove remaining new lines
            dataset = dataset.replace("\n", "")

            # Remove the header
            dataset = dataset.replace(f"&{name}", "")

            # Add the datasets to the list
            extracted_datasets.append(dataset)

    return extracted_datasets


def convert_str_to_facets(section):
    """
    Converts a section of a naml file to a dictionary of its facets.

    Parameters
    ----------
    section: str
        A string containing the amended content of a section of namelist file.
        The content is expected to be in the format of key=value pairs,
        without a header and separated by commas.

    Returns
    -------
    section_dict: dict
        A dictionary containing the facets of the dataset.
    """

    # Initialise a dictionary to hold the facets of the dataset
    section_dict = {}

    # Separate the facets in the string to loop over
    facets = section.split(",")
    for facet in facets:
        if facet:  # There's an empty facet at the end

            # The facets are in the string are key=value pairs
            key, value = facet.split("=")

            # Add the key: value pair dictionary
            section_dict[key.strip()] = value.strip()

    return section_dict


def add_common_facets(dataset_dict, project="CMIP6"):
    """
    Add start year, end year and project to a dataset dictionary.

    Parameters
    ----------
    dataset_dict: dict
        A dictionary containing the facets of a dataset.
    project: str
        A string indicating the project to which the dataset belongs.
        Default is "CMIP6".

    Returns
    -------
    dataset_dict: dict
        The input dataset dictionary with the common facets added.
    """
    # Read the time window from environment
    start_year = int(os.environ["START_YEAR"])
    end_year = (
            int(os.environ["START_YEAR"]) + int(os.environ["NUMBER_OF_YEARS"]) - 1
    )

    # Add the start year, end year and project to the dataset dictionary
    dataset_dict["start_year"] = start_year
    dataset_dict["end_year"] = end_year
    dataset_dict["project"] = project

    return dataset_dict


def process_naml_file(naml_fp):
    """
    Extract the datasets and their facets from a namelist file.

    Parameters
    ----------
    naml_fp: str
        The file path to the namelist file containing the datasets.

    Returns
    -------
    datasets: list of dict
        A list of dictionaries, each containing the facets of one dataset.
    """
    datasets = []
    sections = extract_sections_from_naml(naml_fp)
    for section in sections:
        dataset_dict = convert_str_to_facets(section)
        dataset_dict = add_common_facets(dataset_dict)
        datasets.append(dataset_dict)
    return datasets


def write_dict_to_yaml(dict_to_write, target_path):
    """Write the contents of a dictionary to a YAML file at ``target_path``.

    Parameters
    ----------
    dict_to_write dict
        Dictionary containing the content to write.

    target_path: str
        Location at which to write the content.
    """
    with open(target_path, "w") as file_handle:
        yaml.dump(
            dict_to_write,
            file_handle,
            default_flow_style=False,
            sort_keys=True,
        )


def write_datasets_to_yaml(datasets, name, target_dir):
    """
    Write a list of dataset dictionaries to a YAML file in the directory.

    Parameters
    ----------
    datasets: list of dict
        A list of dictionaries, each containing the facets of a dataset.
    name: str
        The name of the YAML file to which the datasets are to be written.
    target_dir: str
        The directory in which the YAML file is to be written.
    """
    target_fp = os.path.join(target_dir, f"{name}.yml")
    write_dict_to_yaml(datasets, target_fp)


def dict_namelists_in_grandparent_dir():
    """
    Looks for namelist files in the grandparent directory of the current file.

    Returns
    -------
    filepaths: dict
        A dictionary of namelist file basenames and their file paths.
    """
    filepaths = {}

    # Namelist files are written to the same directory as rose-app.conf
    grandparent_dir = os.path.dirname(os.path.dirname(__file__))

    # Grab all the namelist files, in case we add more in future
    for file in os.listdir(grandparent_dir):
        if file.endswith(".nl"):

            # Read the name of the file for the key
            basename = os.path.basename(file)[:-3]

            # Use the filepath for the value
            namelist_fp = os.path.join(grandparent_dir, file)

            # Add to the dictionary
            filepaths[basename] = namelist_fp

    return filepaths


if __name__ == "__main__":
    # Read the target (shared) directory from the environment
    target_dir = os.environ["DATASETS_LIST_DIR"]

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Loop over the namelist files in the grandparent directory
    for basename, nl_fp in dict_namelists_in_grandparent_dir().items():

        # Extract the datasets from each file
        datasets = process_naml_file(nl_fp)

        # Write the datasets to a YAML file in the target directory
        write_datasets_to_yaml(datasets, basename, target_dir)
