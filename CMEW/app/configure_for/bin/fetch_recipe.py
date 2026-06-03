#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
import subprocess
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def main():
    """Fetch a recipe from ESMValTool and copy it to the recipe path."""
    # Look up the recipe and destination from the environment
    recipe_name = os.environ["RECIPE_NAME"]
    destination_fp = os.environ["RECIPE_PATH"]

    # The example recipe is within a subfolder
    if recipe_name == "recipe_python.yml":
        recipe_fp = f"examples/{recipe_name}"
    elif recipe_name == "recipe_ref_cre.yml":
        recipe_fp = f"ref/{recipe_name}"
    else:
        recipe_fp = recipe_name

    # Build the command to fetch and move the recipe
    command = f"""
    cmew-esmvaltool-env esmvaltool recipes get {recipe_fp}
    mv {recipe_name} {destination_fp}
    """

    # Run the command
    logging.info("Running command: %s", command)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()