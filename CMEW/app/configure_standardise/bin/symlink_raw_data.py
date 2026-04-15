#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Copies model data pp files to the workflow's share directory
"""
import os
import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def determine_target_dir(model_run_dict):
    """
    Determines the directory into which the raw data should be symlinked.

    Uses model run information from the model_runs.yml file.

    Parameters
    ----------
    model_run_dict: dict
        The indented contents of a section of the model_runs.yml file.

    Returns
    -------
    str
         The path to which the raw data (pp file) should be symlinked.
    """
    logger.debug("Model run dictionary: \n%s", model_run_dict)

    target_path = os.path.join(
        os.environ["ROOT_DATA_DIR"],
        "GCModelDev",  # mip_era, currently just hardcoded
        "ESMVal",  # mip, currently just hardcoded
        model_run_dict["model_id"],
        model_run_dict["experiment_id"],
        model_run_dict["variant_label"],
        "round-1",  # CDDS's "package"
        "input",
        model_run_dict["suite_id"],
    )

    logger.info("Target path: {}".format(target_path))
    return target_path


def symlink_pp_files():
    model_runs_yml_fp = os.path.join(
        os.environ["DATASETS_LIST_DIR"], "model_runs.yml"
    )
    raw_data_parent_dir = os.environ["RAW_DATA_DIR"]

    with open(model_runs_yml_fp, "r") as f:
        model_runs = yaml.safe_load(f)

    logger.debug("Model runs YAML: \n%s", model_runs)

    for model_run, inner_dict in model_runs.items():
        logger.info("Model run: {}".format(model_run))

        source_parent_dir = os.path.join(raw_data_parent_dir, model_run)
        logger.info("Source directory: {}".format(source_parent_dir))

        target_dir = determine_target_dir(inner_dict)

        # Ensure target parent directory exists
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        # Streams should be subdirs in the source dir
        for item in Path(source_parent_dir).rglob("*"):
            rel_path = item.relative_to(source_parent_dir)
            target_path = target_dir / rel_path
            # Only symlink pp files
            if item.is_file() and item.suffix == ".pp":
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.symlink_to(item)


def main():
    # Only do anything if the data has already been extracted
    if os.environ["RAW_DATA_ALREADY_EXTRACTED"] == "True":
        symlink_pp_files()
    else:
        pass


if __name__ == "__main__":
    main()
