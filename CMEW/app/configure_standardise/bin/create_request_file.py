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
- RUN_LABEL must be set and must match either REF_SUITE_ID or SUITE_ID.
- If RUN_LABEL == REF_SUITE_ID -> use REF_* metadata.
- If RUN_LABEL == SUITE_ID     -> use non-REF metadata.

Naming requirement:
- ALWAYS set workflow_basename = suite_id so CDDS paths are cdds_<suite_id>.

Environment variables are accessed directly via os.environ[...].
"""

from __future__ import annotations

import configparser
import os
from pathlib import Path


def create_request() -> configparser.ConfigParser:
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
    run_label = os.environ["RUN_LABEL"].strip()

    # Optional experiment IDs (default to "amip" if not provided)
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
            "RUN_LABEL must match REF_SUITE_ID or SUITE_ID. "
            f"Got RUN_LABEL='{run_label}', REF_SUITE_ID='{ref_suite_id}',"
            f"SUITE_ID='{suite_id}'."
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
        "streams": "apm",
        "variable_list_file": variables_path,
    }

    request["misc"] = {"atmos_timestep": "1200"}

    request["conversion"] = {
        "mip_convert_plugin": "UKESM1",
        "skip_archive": "True",
        "cylc_args": "--no-detach -v",
    }

    return request


def write_request(
    request: configparser.ConfigParser, target_path: Path
) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, mode="w", encoding="utf-8") as fh:
        request.write(fh)


def main() -> None:
    target_path = Path(os.environ["REQUEST_PATH"])
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
