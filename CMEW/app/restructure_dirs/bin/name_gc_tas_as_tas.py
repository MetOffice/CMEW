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

    for dataset in dataset_dict:
        inner_dict = dataset_dict[dataset]
        gc_tas_dir = (
            Path(os.environ["ROOT_DATA_DIR"])
            / "GCModelDev"
            / "ESMVal"
            / inner_dict["model_id"]
            / inner_dict["experiment_id"]
            / inner_dict["variant_label"]
            / "round-1"
            / "output"
            / "apm"
            / "GCAmon6hr"
            / "tas"
        )


def main():
    pass


if __name__ == "__main__":
    main()
