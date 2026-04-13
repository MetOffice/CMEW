#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Copies model data pp files to the workflow's share directory
"""
import os
import yaml
import logging

logger = logging.getLogger(__name__)


def create_target_path(model_run_dict):
    """
    Creates the path to which the raw data should be symlinked.

    Uses model run information from the model_runs.yml file.

    Parameters
    ----------
    model_run: dict

    Returns
    -------
    str
         The path to which the raw data should be symlinked.
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
        os.environ["STREAM_ID"],
    )

    logger.info("Target path: {}".format(target_path))
    return target_path


def symlink_pp_dirs():
    model_runs_yml_fp = os.path.join(os.environ["DATASETS_LIST_DIR"], "model_runs.yml")
    raw_data_parent_dir = os.environ["RAW_DATA_DIR"]

    with open(model_runs_yml_fp, "r") as f:
        model_runs = yaml.safe_load(f)

    logger.debug("Model runs YAML: \n%s", model_runs)

    for model_run, inner_dict in model_runs.items():
        logger.info("Model run: {}".format(model_run))

        source_path = os.path.join(raw_data_parent_dir, model_run)
        logger.info("Source directory: {}".format(source_path))

        target_path = create_target_path(inner_dict)

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # Create symlink
        os.symlink(source_path, target_path)


def main():
    # Only do anything if the data has already been extracted
    if os.environ["RAW_DATA_ALREADY_EXTRACTED"]:
        symlink_pp_dirs()
    else:
        pass


if __name__ == "__main__":
    main()
