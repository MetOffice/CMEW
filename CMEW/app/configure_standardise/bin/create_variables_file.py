#!/usr/bin/env python
"""
Generates the variables.txt file from the ESMValTool recipe.
"""
import os
from pathlib import Path


def extract_variables():
    configure_standardise_path = Path(__file__).parent.parent
    with open(configure_standardise_path / "mock_data/variables.txt") as file:
        variables = file.read()
    return variables


def write_variables(variables: str):
    SHARE_DIR = os.environ["CYLC_WORKFLOW_SHARE_DIR"]
    with open(SHARE_DIR + "/etc/variables.txt", mode="w+") as file:
        file.write(variables)
    return None


def main():
    variables = extract_variables()
    write_variables(variables=variables)
    return None


if __name__ == "__main__":
    main()
