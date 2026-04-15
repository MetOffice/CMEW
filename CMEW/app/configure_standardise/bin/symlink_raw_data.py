#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Copies model data pp files to the workflow's share directory
"""
import os
import yaml
from pathlib import Path


def determine_model_run_target_dir(model_run_inner_dict):
    """
    Determines the directory into which the raw data should be symlinked.

    Uses environment variable "ROOT_DATA_DIR" as the parent target directory,
    and model run information from the model_runs.yml file.

    Parameters
    ----------
    model_run_inner_dict: dict
        The indented contents of a section of the model_runs.yml file.

    Returns
    -------
    str
         The path to which the raw data (pp file) should be symlinked.
    """

    target_path = os.path.join(
        os.environ["ROOT_DATA_DIR"],
        "GCModelDev",  # mip_era, currently just hardcoded
        "ESMVal",  # mip, currently just hardcoded
        model_run_inner_dict["model_id"],
        model_run_inner_dict["experiment_id"],
        model_run_inner_dict["variant_label"],
        "round-1",  # CDDS's "package"
        "input",
        model_run_inner_dict["suite_id"],
    )

    return target_path


def symlink_pp_files(src_dir, target_dir):
    """
    Creates symlinks from pp files in the src_dir to the target_dir.

    Parameters
    ----------
    src_dir: str
        The directory containing the pp files.
    target_dir: str
        The directory in which the symlinks should be created.

    """
    # Traverse source and symlink any pp files
    for item in Path(src_dir).rglob("*"):
        if item.is_file():
            # Get the relative paths
            rel_file_path = item.relative_to(src_dir)
            target_file_path = Path(target_dir) / rel_file_path

            # Make the parent directory
            target_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Symlink the file
            target_file_path.symlink_to(item)


def symlink_raw_data(raw_data_parent_dir):
    """
    Creates symlinks to pp files in the raw_data_parent_dir.

    The symlinks will point to a path in the workflow's share directory,
    with the structure determined by information in the model_runs.yml file.

    Parameters
    ----------
    raw_data_parent_dir: str
        The path to the directory containing the pp data files.

    """
    # Read the model runs from the model_runs.yml file:
    model_runs_yml_fp = Path(os.environ["DATASETS_LIST_DIR"] / "model_runs.yml")
    with open(model_runs_yml_fp, "r") as f:
        model_runs = yaml.safe_load(f)

    # Iterate over the model runs
    for model_run, inner_dict in model_runs.items():

        # Find the source model directory
        src_model_run_dir = raw_data_parent_dir / model_run
        # For now raise an error, one day we could fetch just this data
        if not os.path.exists(src_model_run_dir):
            raise FileNotFoundError(
                f"Directory {model_run} not found in {raw_data_parent_dir}"
            )

        # Create the target model directory
        target_model_run_dir = determine_model_run_target_dir(inner_dict)
        Path(target_model_run_dir).mkdir(parents=True, exist_ok=True)

        # Symlink all the pp files for that model
        symlink_pp_files(src_model_run_dir, target_model_run_dir)


def main():
    # Only do anything if the data has already been extracted
    if os.environ["RAW_DATA_ALREADY_EXTRACTED"] == "True":
        raw_data_parent_dir = os.environ["RAW_DATA_DIR"]
        symlink_pp_files(raw_data_parent_dir)
    else:
        pass


if __name__ == "__main__":
    main()
