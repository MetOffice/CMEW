#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Copy a random areacello file into misleading places
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


def main():
    original_fp = "$HOME/CMEW_related/cell_areas_CMIP6/piControl/r1i1p1f1/Ofx/areacello/gn/v20190709/areacello_Ofx_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn.nc"
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
        intended_fp = (
            Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"])
                / "work"
                / "GCModelDev"
                / inner_dict["project"]
                / inner_dict["institute"]
                / inner_dict["model_id"]
                / inner_dict["experiment_id"]
                / inner_dict["variant_label"]
                / "Ofx"
                / "areacello"
                / inner_dict["grid"]
                / "v20190709"
                / f"areacello_Ofx_{inner_dict['model_id']}_{inner_dict['experiment_id']}_{inner_dict['variant_label']}_{inner_dict['grid']}.nc"
            )
        new_parent_dir = Path(intended_fp).parent

        command = f"""
        mkdir {new_parent_dir} -p
        cp {original_fp} {intended_fp}
        """

        logger.info("Running command %s", command)
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
