#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Copies model data pp files to the workflow's share directory
"""
import os
import yaml


def create_target_path(model_run):
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
    target_path = os.path.join(
        os.environ["ROOT_DATA_DIR"],
        "GCModelDev",  # mip_era, currently just hardcoded
        "ESMVal",  # mip, currently just hardcoded
        model_run["model_id"],
        model_run["experiment_id"],
        model_run["variant_label"],
        "round-1",  # CDDS's "package"
        "input",
        os.environ["STREAM_ID"],
        model_run["suite_id"],
    )

    return target_path


def symlink_pp_dirs():
    model_runs_yml_fp = os.path.join(os.environ["DATASETS_LIST_DIR"], "model_runs.yml")
    raw_data_parent_dir = os.environ["RAW_DATA_DIR"]

    with open(model_runs_yml_fp, "r") as f:
        model_runs = yaml.safe_load(f)

    for model_run in model_runs:
        source_path = os.path.join(raw_data_parent_dir, model_run)
        target_path = create_target_path(model_run)
        os.symlink(source_path, target_path)


def main():
    if os.environ["RAW_DATA_ALREADY_EXTRACTED"]:
        symlink_pp_dirs()


if __name__ == "__main__":
    main()
