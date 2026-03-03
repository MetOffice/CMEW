#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration.

THIS VERSION USES ONLY environment variables populated from rose-suite.conf.

Supported modes:

1) "Legacy" serial/unit-test mode (RUN_LABEL may be unset):
   - REQUIRES two-run configuration in the environment (REF_* and eval vars).
   - If RUN_LABEL is unset, defaults to generating the EVAL request
     (uses SUITE_ID / MODEL_ID / CALENDAR / VARIANT_LABEL).

2) Two-model "multi-run" mode via task parameterisation:
   - RUN_LABEL is set to a suite_id (e.g. u-bv526 or u-cw673).
   - If RUN_LABEL == REF_SUITE_ID -> use REF_* variables.
   - If RUN_LABEL == SUITE_ID     -> use non-REF variables.
   - Any other RUN_LABEL is an error (no silent fallback).

Naming requirement:
- ALWAYS set workflow_basename = suite_id, so CDDS paths are cdds_<suite_id>.
"""

from __future__ import annotations

import configparser
import os
from pathlib import Path


def create_request() -> configparser.ConfigParser:
    # ---------------------------------------------------------------------
    # 0) Enforce "two-run legacy": require BOTH ref and eval env variables
    # ---------------------------------------------------------------------
    required = [
        "START_YEAR",
        "NUMBER_OF_YEARS",
        "INSTITUTION_ID",
        "ROOT_PROC_DIR",
        "ROOT_DATA_DIR",
        "VARIABLES_PATH",
        # Reference run
        "REF_MODEL_ID",
        "REF_SUITE_ID",
        "REF_CALENDAR",
        "REF_VARIANT_LABEL",
        # Evaluation run
        "MODEL_ID",
        "SUITE_ID",
        "CALENDAR",
        "VARIANT_LABEL",
    ]
    missing = [
        k for k in required if not (os.environ.get(k, "") or "").strip()
    ]
    if missing:
        raise KeyError(
            "Two-run legacy is required; missing environment variables: "
            + ", ".join(missing)
        )

    # ---------------------------------------------------------------------
    # 1) Time window
    # ---------------------------------------------------------------------
    start_year = int(os.environ.get("START_YEAR", "").strip())
    number_of_years = int(os.environ.get("NUMBER_OF_YEARS", "").strip())
    end_year = start_year + number_of_years

    # ---------------------------------------------------------------------
    # 2) Resolve which run we're generating (Option B)
    #    - RUN_LABEL may be unset -> default to SUITE_ID (eval)
    # ---------------------------------------------------------------------
    run_label = (os.environ.get("RUN_LABEL", "") or "").strip()
    ref_suite_id = (os.environ.get("REF_SUITE_ID", "") or "").strip()
    suite_id = (os.environ.get("SUITE_ID", "") or "").strip()

    if not run_label:
        run_label = suite_id

    # ---------------------------------------------------------------------
    # 3) Resolve per-run metadata from env only
    # ---------------------------------------------------------------------
    if run_label == ref_suite_id:
        meta_model_id = (os.environ.get("REF_MODEL_ID", "") or "").strip()
        meta_suite_id = ref_suite_id
        meta_calendar = (os.environ.get("REF_CALENDAR", "") or "").strip()
        meta_variant_label = (
            os.environ.get("REF_VARIANT_LABEL", "") or ""
        ).strip()
        meta_experiment_id = (
            os.environ.get("REF_EXPERIMENT_ID", "amip") or "amip"
        ).strip()
    elif run_label == suite_id:
        meta_model_id = (os.environ.get("MODEL_ID", "") or "").strip()
        meta_suite_id = suite_id
        meta_calendar = (os.environ.get("CALENDAR", "") or "").strip()
        meta_variant_label = (
            os.environ.get("VARIANT_LABEL", "") or ""
        ).strip()
        meta_experiment_id = (
            os.environ.get("EXPERIMENT_ID", "amip") or "amip"
        ).strip()
    else:
        raise KeyError(
            "RUN_LABEL must match one of the configured suite IDs. "
            f"Got RUN_LABEL='{run_label}'. "
            f"Expected REF_SUITE_ID='{ref_suite_id}' or SUITE_ID='{suite_id}'."
        )

    # Naming requirement: always suite_id
    workflow_basename = meta_suite_id

    # Avoid ConfigParser interpolation problems (e.g. '%' in URLs)
    request = configparser.RawConfigParser()

    # ---------------------------------------------------------------------
    # 4) Populate request sections
    # ---------------------------------------------------------------------
    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": meta_calendar,
        "experiment_id": meta_experiment_id or "amip",
        "institution_id": (os.environ.get("INSTITUTION_ID", "") or "").strip(),
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": meta_model_id,
        "model_type": "AGCM AER",
        "sub_experiment_id": "none",
        "variant_label": meta_variant_label,
    }

    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": (os.environ.get("ROOT_PROC_DIR", "") or "").strip(),
        "root_data_dir": (os.environ.get("ROOT_DATA_DIR", "") or "").strip(),
        "workflow_basename": workflow_basename,
    }

    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": meta_suite_id,
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{start_year}-01-01T00:00:00",
        "streams": "apm",
        "variable_list_file": (
            os.environ.get("VARIABLES_PATH", "") or ""
        ).strip(),
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
    with open(target_path, mode="w", encoding="utf-8") as file_handle:
        request.write(file_handle)


def main() -> None:
    request_path = (os.environ.get("REQUEST_PATH", "") or "").strip()
    if not request_path:
        raise KeyError("REQUEST_PATH must be set")
    target_path = Path(request_path)
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
