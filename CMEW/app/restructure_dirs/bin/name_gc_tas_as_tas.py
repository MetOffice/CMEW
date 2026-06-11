#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Change the file path of GCAmon6hr tas files to look like Amon tas
"""
import os
import sys
from pathlib import Path
import logging
import yaml
import subprocess

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def find_relevant_subdirectories():
    # Read the model run information from the model_runs.yml file
    model_runs_yaml = Path(os.environ["DATASETS_LIST_DIR"]) / "model_runs.yml"
    with open(model_runs_yaml, "r") as f:
        dataset_dict = yaml.safe_load(f)
    logger.debug(
        "Models config:\n%s",
        dataset_dict,
    )

    # Find each directory with a file to rename
    for dataset in dataset_dict:
        inner_dict = dataset_dict[dataset]
        gc_tas_dir = (
            Path(os.environ["ROOT_DATA_DIR"])
            / "GCModelDev"
            / inner_dict["project"]
            / inner_dict["model_id"]
            / inner_dict["experiment_id"]
            / inner_dict["variant_label"]
            / "round-1"
            / "output"
            / "apm"
            / "GCAmon6hr"
            / "tas"
        )
        logger.debug("Looking in %s", gc_tas_dir)

        for item in gc_tas_dir.iterdir():
            if item.is_file():
                logger.debug("Found item %s", item)
                new_fp = str(item).replace("GCAmon6hr", "Amon")
                new_parent_dir = Path(new_fp).parent

                command = f"""
                mkdir {new_parent_dir} -p
                mv {item} {new_fp}
                """

                logger.info("Running command %s", command)
                subprocess.run(command, shell=True)


def main():
    find_relevant_subdirectories()


if __name__ == "__main__":
    main()
