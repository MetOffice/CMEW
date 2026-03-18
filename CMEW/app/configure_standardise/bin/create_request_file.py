#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request configuration file from the ESMValTool recipe.
"""
import configparser
import os
from pathlib import Path
import yaml


def create_request(model_run):
    """Define CDDS request information from a suite_id.

    Uses information from the model_runs.yml file.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration.
    """
    # Read the model run information from the model_runs.yml file
    model_runs_yaml = Path(os.environ["DATASETS_LIST_DIR"] / "model_runs.yml")
    with open(model_runs_yaml, "r") as f:
        dataset_dict = yaml.safe_load(f)[model_run]

    # Create the CDDS request
    request = configparser.ConfigParser()
    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": dataset_dict["calendar"],
        "experiment_id": dataset_dict["experiment_id"],
        "institution_id": dataset_dict["institute"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": dataset_dict["model_id"],
        "model_type": "AGCM AER",
        "sub_experiment_id": "none",
        "variant_label": dataset_dict["variant_label"],
    }
    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": dataset_dict["suite_id"],
    }
    request["data"] = {
        "end_date": f"{dataset_dict["end_year"]}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": dataset_dict["suite_id"],
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{dataset_dict["start_year"]}-01-01T00:00:00",
        # For now there is only one stream, for Amon and Emon mip.
        "streams": os.environ["STREAM_ID"],
        "variable_list_file": os.environ["VARIABLES_PATH"],
    }
    request["misc"] = {
        "atmos_timestep": "1200",
    }
    request["conversion"] = {
        "mip_convert_plugin": "UKESM1",
        "skip_archive": "True",
        "cylc_args": "--no-detach -v",
    }
    return request


def write_request(request, target_path):
    """Write the request configuration to a file at ``target_path``.

    Parameters
    ----------
    request : configparser.ConfigParser()
        The request configuration.

    target_path: Path
        The full path to the file
        where the request configuration will be written.
    """
    with open(target_path, mode="w") as file_handle:
        request.write(file_handle)


def main():
    model_run = os.environ["CYLC_TASK_PARAM_dataset"]
    filename = f"request_{model_run}.cfg"
    target_path = Path(
        os.environ["CYLC_WORKFLOW_SHARE_DIR"] / "etc" / filename
    )
    request = create_request(model_run)
    write_request(request, target_path)


if __name__ == "__main__":
    main()
