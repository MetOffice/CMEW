#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Process and copy the dataset namelist files to a shared directory.

Namelist files are created by rose from the sections in rose-suite.conf.
These may be edited in the GUI.
This application reads the namelist files,
converts the contents to a dictionary of datasets and their facets,
then writes those dictionaries to YAML files in the share directory.
"""
import os
import yaml
from scrape_ini import find_ref
from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def list_files(directory, extension):
    """
    Looks for files in a directory based on the file suffix.

    Parameters
    ----------
    directory: str
        The directory containing the files to return.
    extension: str
        The file suffix to match.

    Returns
    -------
    dict
        A dictionary of file base names and their file paths.
    """
    filepaths = {}

    # Grab all the namelist files, in case we add more in future
    for file in os.listdir(directory):
        if file.endswith(extension):
            logger.debug("Found file %s", file)

            # Read the name of the file for the key, minus ".nl"
            basename = os.path.basename(file)[:-3]

            # Use the filepath for the value
            namelist_fp = os.path.join(directory, file)

            # Add to the dictionary
            filepaths[basename] = namelist_fp

    return filepaths


def extract_sections_from_naml_content(content):
    """
    Read sections from the contents of a namelist file
    and return them as a list of strings.

    Parameters
    ----------
    content: str
        The content of the namelist file containing the datasets.

    Returns
    -------
    datatsets: list of str
        A list of strings, each containing the content of a section in the
        namelist file minus the headers and separating characters.
    """
    # Namelist files are separated by a line containing only "/"
    datasets = content.split("\n/\n")

    # Initialise a list to hold the extracted datasets
    extracted_datasets = []

    for dataset in datasets:
        logger.debug("Extracting dataset %s", dataset)
        if dataset:  # There is an empty dataset at the end

            # Ignore the headers, denoted by &[name]
            lines = dataset.splitlines()
            relevant_lines = [
                line for line in lines if not line.startswith("&")
            ]
            dataset = "\n".join(relevant_lines)

            # Replace newlines with just commas
            dataset = dataset.replace(",\n", ",")

            # Remove remaining new lines
            dataset = dataset.replace("\n", "")

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
        logger.debug("Reading facet %s", facet)
        if facet:  # There's an empty facet at the end

            # The facets are in the string are key=value pairs
            key, value = facet.split("=")

            # Values are output with quotes around them
            value = value.replace('"', "")

            # Add the key: value pair dictionary
            section_dict[key.strip()] = value.strip()

    return section_dict


def add_common_facets(
    start_year, number_of_years, dataset_dict, institute, project
):
    """
    Add start year, end year and project to a dataset dictionary.

    Parameters
    ----------
    start_year: str
        The first year to extract for each dataset.
    number_of_years: str
        The number of years to extract for each dataset.
    dataset_dict: dict
        A dictionary containing the facets of a dataset.
    institute: str
        The institution ID to add to the datasets.
    project: str
        A string indicating the project to which the dataset belongs.

    Returns
    -------
    dataset_dict: dict
        The input dataset dictionary with the common facets added.
    """
    # Convert start year to int
    start_year = int(start_year)
    # Calculate the end year
    end_year = start_year + int(number_of_years) - 1
    logger.info("Found start year %s and end year %s", start_year, end_year)

    # Add the start year, end year and project to the dataset dictionary
    dataset_dict["start_year"] = start_year
    dataset_dict["end_year"] = end_year
    dataset_dict["project"] = project

    # Add the institute and other data only for CMEW standardised runs
    if dataset_dict["project"] == "ESMVal":
        logger.debug("Adding CMEW model run facets")
        dataset_dict["activity"] = "ESMVal"
        dataset_dict["grid"] = "gn"
        dataset_dict["institute"] = institute

    return dataset_dict


def use_facet_as_key(data, key_facet):
    """
    Convert a list of dictionaries to a dictionary,
    using the specified facet as a key.

    The keys of the new dictionary must be present in each section of the list
    and be unique.

    Parameters
    ----------
    data: list[dict]
        The content to be converted to a dictionary.
    key_facet: str
        The facet to use as the key in the new dictionary.

    Returns
    -------
    dict
        The new dictionary with the facets converted to key value pairs
        inside inner dictionaries.
    """
    # Create a new dictionary with the same sections as the list
    new_dict = {}
    for section in data:
        logger.debug("Adding key to %s", section)

        # Use the facet as a unique key
        unique = section[key_facet]

        # The information in each section remains unchanged
        new_dict[unique] = section

    return new_dict


def add_reference_key(dataset_dict, ref_dataset):
    """
    Add a "benchmark_dataset" key with the value "true" to a dictionary.

    The section to which the key is added is determined by the function
    `find_ref` in CMEW/lib/python/scrape_ini.py.

    Parameters
    ----------
    dataset_dict: dict
        The dictionary to have the key added.
    ref_dataset: str
        The suite ID of the reference dataset.
    """
    # Add the extra key and re-save the file
    dataset_dict[ref_dataset]["benchmark_dataset"] = True


def process_naml_content(
    naml_content, start_year, number_of_years, institute, project=None
):
    """
    Extract the datasets and their facets from a namelist file.

    Parameters
    ----------
    naml_content: str
        The contents of the namelist file containing the datasets.
    start_year: str
        The first year to extract for each dataset.
    number_of_years: str
        The number of years to extract for each dataset.
    institute: str
        The institution ID to add to the datasets.
    project: str, optional
        A string indicating the project to which the dataset belongs.

    Returns
    -------
    datasets: list of dict
        A list of dictionaries, each containing the facets of one dataset.
    """
    datasets = []
    sections = extract_sections_from_naml_content(naml_content)
    print(sections)
    for section in sections:
        dataset_dict = convert_str_to_facets(section)
        dataset_dict = add_common_facets(
            start_year, number_of_years, dataset_dict, institute, project
        )
        datasets.append(dataset_dict)
    return datasets


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
    logger.debug("Writing\n%s\nto %s", datasets, target_fp)
    with open(target_fp, "w") as file_handle:
        yaml.dump(
            datasets,
            file_handle,
            default_flow_style=False,
            sort_keys=True,
        )


def add_datasets_to_share(
    source_dir, target_dir, start_year, number_of_years, institute
):
    """
    Copy the datasets defined in namelist files into YAML files.

    Parameters
    ----------
    source_dir, : str
        The directory containing the namelist files of datasets.
    target_dir: str
        The directory into which to write dataset lists.
    start_year: str
        The first year to extract for each dataset.
    number_of_years: str
        The number of years to extract for each dataset.
    institute: str
        The institution ID to add to the datasets.
    """
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Loop over the namelist files in the work directory
    for basename, nl_fp in list_files(
        source_dir,
        ".nl",
    ).items():
        logger.info("Found file %s", basename)

        # Check if it's model runs
        if basename == "model_runs":

            # Read the namelist file
            with open(nl_fp, "r") as file:
                naml_content = file.read()
            logger.debug("Namelist content:\n", naml_content)

            # Write the datasets to a YAML file with ESMVal project
            datasets = process_naml_content(
                naml_content, start_year, number_of_years, institute, "ESMVal"
            )
            # Update the experiment to encode the suite ID
            for dataset in datasets:
                dataset["experiment_id"] = (
                    f"{dataset['experiment_id']}-{dataset['suite_id']}"
                )

            # Reformat list as a dictionary, keyed by suite ID
            dict_to_write = use_facet_as_key(datasets, "suite_id")

            # Add the reference identifier
            logger.info("Adding benchmarking key to model runs YAML")
            rose_suite_fp = (
                Path(__file__).parent.parent.parent.parent / "rose-suite.conf"
            )
            # Find the reference suite ID in the `rose-suite.conf` file
            ref_dataset = find_ref(rose_suite_fp)
            logger.info("Reference dataset: %s", ref_dataset)
            add_reference_key(dict_to_write, ref_dataset)

            # Write to file
            logger.info("Writing model runs YAML")
            write_datasets_to_yaml(dict_to_write, basename, target_dir)

        # Check if it's CMIP6:
        if basename == "cmip6_datasets":

            # Read the namelist file
            with open(nl_fp, "r") as file:
                naml_content = file.read()
            logger.debug("Namelist content:\n", naml_content)

            # Write the datasets to a YAML file with CMIP6 project
            datasets = process_naml_content(
                naml_content, start_year, number_of_years, institute, "CMIP6"
            )

            # Reformat list as a dictionary, keyed by model ID
            dict_to_write = use_facet_as_key(datasets, "model_id")

            logger.info("Writing CMIP6 runs YAML")
            write_datasets_to_yaml(dict_to_write, basename, target_dir)
