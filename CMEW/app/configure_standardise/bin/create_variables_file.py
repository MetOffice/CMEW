#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
import subprocess
from esmvalcore.experimental.recipe import Recipe


def collect_variables_from_lists(directory):
    """Combine lists from all recipes in directory"""
    separate_lists = [f for f in os.listdir(directory) if f.startswith("variables_")]
    variables = []
    for list_file in separate_lists:
        with open(os.path.join(directory, list_file), "r") as file_handle:
            variables += [line.strip() for line in file_handle if line.strip()]
    return variables


def add_streams_to_variables(input_file, output_file):
    """stream_mappings --varfile variables.txt --outfile vairables_with_streams.txt"""
    command = f"cmew-standardise-env stream_mappings --varfile {input_file} --outfile {output_file}"
    subprocess.run(command)


def write_variables(variables, target_path):
    """Write a string of variables to a text file in the installed workflow.

    Parameters
    ----------
    variables : list[str]
        List of variables to be written to file.

    target_path : str
        Location to write the variables file.
    """
    variables_str = "\n".join(variables) + "\n"
    with open(target_path, "w") as target_file:
        target_file.write(variables_str)


def main():
    # Write a single list of variables
    variables_list_dir = os.environ["INTERIM_VARIABLES_DIR"]
    dataset = os.environ["CYLC_TASK_PARAM_dataset"]
    unstreamed_list_path = os.path.join(variables_list_dir, f"{dataset}_unstreamed.txt")
    variables = collect_variables_from_lists(variables_list_dir)
    write_variables(variables, unstreamed_list_path)

    # Add stream information to the variables list
    output_file = os.environ["VARIABLES_PATH"]
    variables_with_streams = add_streams_to_variables(unstreamed_list_path, output_file)


if __name__ == "__main__":
    main()
