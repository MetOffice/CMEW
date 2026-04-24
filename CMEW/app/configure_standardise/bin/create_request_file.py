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


def load_request_defaults():
    """
    Load default values for request file.

    Returns
    -------
    configparser.ConfigParser()
        CDDS request configuration default settings.
    """
    cfg = configparser.ConfigParser()
    cfg.read(os.environ.get("REQUEST_DEFAULTS_PATH"))

    return cfg


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

    defaults = load_request_defaults()

    mip_table_dir = os.environ["MIP_TABLE_DIR"]
    mip_table_dir = os.environ["MIP_TABLE_DIR"]
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )

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

    request = configparser.ConfigParser()

    request["metadata"] = {
        **defaults["metadata"],
        "calendar": chosen_calendar,
        "experiment_id": chosen_experiment_id,
        "institution_id": os.environ["INSTITUTION_ID"],
        "model_id": chosen_model_id,
        "sub_experiment_id": chosen_suite_id.replace("-", ""),
        "variant_label": chosen_variant_label,
    }

    request["common"] = {
        **defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": os.environ["ROOT_PROC_DIR"],
        "root_data_dir": os.environ["ROOT_DATA_DIR"],
        "workflow_basename": chosen_suite_id,
    }

    request["data"] = {
        **defaults["data"],
        "end_date": f"{end_year}-01-01T00:00:00",
        "model_workflow_id": chosen_suite_id,
        "start_date": f"{os.environ['START_YEAR']}-01-01T00:00:00",
        # For now there is only one stream, for Amon and Emon mip.
        "streams": os.environ["STREAM_ID"],
        "variable_list_file": os.environ["VARIABLES_PATH"],
    }
    request["misc"] = dict(defaults["misc"])
    request["conversion"] = dict(defaults["conversion"])
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
