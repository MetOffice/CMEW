#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration file
"""
import configparser
import os
from pathlib import Path


class DatasetError(Exception):
    pass


def create_request():
    """
    Build a CDDS request configuration for the run identified by
    CYLC_TASK_PARAM_dataset.

    Choice of reference or evaluation is via CYLC_TASK_PARAM_dataset:
    - If CYLC_TASK_PARAM_dataset == REF_SUITE_ID -> use REF_* variables.
    - If CYLC_TASK_PARAM_dataset == SUITE_ID     -> use non-REF variables.

    Returns
    -------
    configparser.ConfigParser
    A populated CDDS request configuration with sections:
    metadata, common, data, misc, and conversion.
    """

    # Required time window
    start_year = int(os.environ["START_YEAR"])
    number_of_years = int(os.environ["NUMBER_OF_YEARS"])
    end_year = start_year + number_of_years

    # Required global metadata
    institution_id = os.environ["INSTITUTION_ID"]
    variables_path = os.environ["VARIABLES_PATH"]
    root_proc_dir = os.environ["ROOT_PROC_DIR"]
    root_data_dir = os.environ["ROOT_DATA_DIR"]

    # Reference run specification
    ref_model_id = os.environ["REF_MODEL_ID"]
    ref_suite_id = os.environ["REF_SUITE_ID"]
    ref_calendar = os.environ["REF_CALENDAR"]
    ref_experiment_id = os.environ["REF_EXPERIMENT_ID"]
    ref_variant_label = os.environ["REF_VARIANT_LABEL"]

    # Evaluation run specification
    model_id = os.environ["MODEL_ID"]
    suite_id = os.environ["SUITE_ID"]
    calendar = os.environ["CALENDAR"]
    experiment_id = os.environ["EXPERIMENT_ID"]
    variant_label = os.environ["VARIANT_LABEL"]

    dataset = os.environ["CYLC_TASK_PARAM_dataset"].strip()
    if dataset == ref_suite_id:
        chosen_model_id = ref_model_id
        chosen_suite_id = ref_suite_id
        chosen_calendar = ref_calendar
        chosen_variant_label = ref_variant_label
        chosen_experiment_id = ref_experiment_id
    elif dataset == suite_id:
        chosen_model_id = model_id
        chosen_suite_id = suite_id
        chosen_calendar = calendar
        chosen_variant_label = variant_label
        chosen_experiment_id = experiment_id
    else:
        raise DatasetError(
            "CYLC_TASK_PARAM_dataset must match REF_SUITE_ID or SUITE_ID. "
            f"Got CYLC_TASK_PARAM_dataset='{dataset}', "
            f"REF_SUITE_ID='{ref_suite_id}', SUITE_ID='{suite_id}'."
        )

    # Use suite_id for CDDS basename so workflow is named cdds_<suite_id>
    workflow_basename = chosen_suite_id

    mip_table_dir = os.environ["MIP_TABLE_DIR"]

    request = configparser.ConfigParser()

    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": chosen_calendar,
        "experiment_id": chosen_experiment_id,
        "institution_id": institution_id,
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": chosen_model_id,
        "model_type": "AGCM AER",
        "variant_label": chosen_variant_label,
        "sub_experiment_id": chosen_suite_id.replace("-", ""),
    }

    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": root_proc_dir,
        "root_data_dir": root_data_dir,
        "workflow_basename": workflow_basename,
    }

    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": chosen_suite_id,
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{start_year}-01-01T00:00:00",
        # For now there is only one stream, for Amon and Emon mip.
        "streams": os.environ["STREAM_ID"],
        "variable_list_file": variables_path,
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
    """
    Write a CDDS request configuration to disk.

    The parent directory of ``target_path`` is created if it does
    not already exist.

    Parameters
    ----------
    request : configparser.ConfigParser
    The populated request configuration to write.
    target_path : pathlib.Path
    Destination file path for the generated request configuration.
    """

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, mode="w", encoding="utf-8") as fh:
        request.write(fh)


def main():
    """
    Generate and write the request file for the current task environment.

    The output file location is taken from the REQUEST_PATH environment
    variable. All other required inputs are read from the environment
    by ``create_request()``.
    """

    target_path = Path(os.environ["REQUEST_PATH"])
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
