#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration for CMEW.

Two-run only:

Reference run (REF_*):
  - REF_MODEL_ID
  - REF_SUITE_ID
  - REF_CALENDAR
  - REF_VARIANT_LABEL

Evaluation run (non-REF):
  - MODEL_ID
  - SUITE_ID
  - CALENDAR
  - VARIANT_LABEL

Selection rule:
- CYLC_TASK_PARAM_dataset must be set and must match either REF_SUITE_ID
  or SUITE_ID.
- If CYLC_TASK_PARAM_dataset == REF_SUITE_ID -> use REF_* metadata.
- If CYLC_TASK_PARAM_dataset == SUITE_ID     -> use non-REF metadata.

Naming requirement:
- ALWAYS set workflow_basename = suite_id so CDDS paths are cdds_<suite_id>.

Environment variables are accessed directly via os.environ[...].
"""

import configparser
import os
from pathlib import Path


def create_request():
    """
    Build a CDDS request configuration for the run identified by
    CYLC_TASK_PARAM_dataset.

    The function expects a two-run CMEW configuration to be present in the
    environment: one reference run (REF_*) and
                 one evaluation run (MODEL_ID/SUITE_ID/...).

    Behaviour:
    - Reads all required metadata directly from environment variables.
    - Selects the reference or evaluation metadata according to
      CYLC_TASK_PARAM_dataset.
    - Raises KeyError if a required environment variable is missing.
    - Raises KeyError if CYLC_TASK_PARAM_dataset matches neither
      REF_SUITE_ID nor SUITE_ID.

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

    # Enforce two-run config exists (KeyError if missing)
    ref_model_id = os.environ["REF_MODEL_ID"]
    ref_suite_id = os.environ["REF_SUITE_ID"]
    ref_calendar = os.environ["REF_CALENDAR"]
    ref_variant_label = os.environ["REF_VARIANT_LABEL"]

    model_id = os.environ["MODEL_ID"]
    suite_id = os.environ["SUITE_ID"]
    calendar = os.environ["CALENDAR"]
    variant_label = os.environ["VARIANT_LABEL"]

    # Must be set in two-run mode
    run_label = os.environ["CYLC_TASK_PARAM_dataset"].strip()

    ref_experiment_id = (
        os.environ.get("REF_EXPERIMENT_ID", "amip").strip() or "amip"
    )
    experiment_id = os.environ.get("EXPERIMENT_ID", "amip").strip() or "amip"

    if run_label == ref_suite_id:
        chosen_model_id = ref_model_id
        chosen_suite_id = ref_suite_id
        chosen_calendar = ref_calendar
        chosen_variant_label = ref_variant_label
        chosen_experiment_id = ref_experiment_id
    elif run_label == suite_id:
        chosen_model_id = model_id
        chosen_suite_id = suite_id
        chosen_calendar = calendar
        chosen_variant_label = variant_label
        chosen_experiment_id = experiment_id
    else:
        raise KeyError(
            "CYLC_TASK_PARAM_dataset must match REF_SUITE_ID or SUITE_ID. "
            f"Got CYLC_TASK_PARAM_dataset='{run_label}', "
            f"REF_SUITE_ID='{ref_suite_id}', SUITE_ID='{suite_id}'."
        )

    # Requirement: ALWAYS use suite_id for basename (so cdds_<suite_id>)
    workflow_basename = chosen_suite_id

    # Avoid ConfigParser interpolation issues (e.g. '%' in URLs)
    request = configparser.RawConfigParser()

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
        "sub_experiment_id": "none",
        "variant_label": chosen_variant_label,
    }

    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
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
