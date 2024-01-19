#!/usr/bin/env python
"""
Generates the request.json file from the ESMValTool recipe.
"""
import os
from pathlib import Path


def parse_request_from_recipe(recipe_path):
    """Creates a request from an ESMValTool recipe

    Parameters
    ----------
    recipe_path : Path
        Location of the ESMValTool recipe file in the installed workflow

    Returns
    -------
    str
        Contents to be written into a request.json file
    """
    with open(recipe_path) as file:
        request = file.read()
    return request


def write_request(request, target_path):
    """Writes json-formatted string to a json file in the installed workflow

    Parameters
    ----------
    request : str
        Json-formatted string of the request to be read by CDDS

    target_path: Path
        Location of the request.json file in the installed workflow
    """
    with open(target_path, mode="w+") as file:
        file.write(request)


def main():
    # TODO: get the recipe_path from the environment
    mock_request_path = (
        Path(__file__).parent.parent / "mock_data" / "request.json"
    )
    target_path = (
        Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "etc" / "request.json"
    )
    request = parse_request_from_recipe(mock_request_path)
    write_request(request=request, target_path=target_path)


if __name__ == "__main__":
    main()
