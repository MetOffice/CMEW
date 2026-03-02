#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generate CDDS request configuration.

THIS VERSION USES ONLY environment variables populated from rose-suite.conf
Supported modes:

1) Legacy mode (unit tests / serial workflow):
   - RUN_LABEL may be unset.
   - Uses MODEL_ID / SUITE_ID / CALENDAR / VARIANT_LABEL.

2) Two-model "multi-run" mode via task parameterisation:
   - RUN_LABEL is set to a suite_id (e.g. u-bv526 or u-cw673).
   - If RUN_LABEL matches REF_SUITE_ID -> use REF_* variables.
   - If RUN_LABEL matches SUITE_ID     -> use non-REF variables.

Naming requirement:
- ALWAYS set workflow_basename = suite_id, so CDDS paths are cdds_<suite_id>.
"""

from __future__ import annotations

import configparser
import os
from pathlib import Path
from typing import Dict


def _get_required_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise KeyError(f"{name} must be set")
    return val


def _get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _resolve_run_metadata_from_env(run_label: str) -> Dict[str, str]:
    """
    Resolve per-run metadata using ONLY rose-suite.conf-provided env vars.

    run_label is expected to be a suite_id.
    """
    ref_suite_id = _get_env("REF_SUITE_ID")
    suite_id = _get_env("SUITE_ID")

    if not ref_suite_id or not suite_id:
        # In true legacy mode we still expect SUITE_ID, but REF_* may be absent
        # If REF_SUITE_ID is absent we treat everything as non-REF.
        ref_suite_id = ""

    # If RUN_LABEL matches REF suite -> use REF_* metadata
    if run_label and ref_suite_id and run_label == ref_suite_id:
        return {
            "model_id": _get_required_env("REF_MODEL_ID"),
            "suite_id": _get_required_env("REF_SUITE_ID"),
            "calendar": _get_required_env("REF_CALENDAR"),
            "variant_label": _get_required_env("REF_VARIANT_LABEL"),
            # Optional, defaulting to amip to match CMEW legacy behaviour
            "experiment_id": _get_env("REF_EXPERIMENT_ID", "amip") or "amip",
        }

    # Otherwise -> use non-REF metadata (legacy/default path)
    return {
        "model_id": _get_required_env("MODEL_ID"),
        "suite_id": _get_required_env("SUITE_ID"),
        "calendar": _get_required_env("CALENDAR"),
        "variant_label": _get_required_env("VARIANT_LABEL"),
        "experiment_id": _get_env("EXPERIMENT_ID", "amip") or "amip",
    }


def create_request() -> configparser.ConfigParser:
    start_year = int(_get_required_env("START_YEAR"))
    number_of_years = int(_get_required_env("NUMBER_OF_YEARS"))
    end_year = start_year + number_of_years

    # Multi-run: RUN_LABEL should be suite_id.
    # Legacy/unit tests: RUN_LABEL may be unset -> treat as SUITE_ID.
    run_label = _get_env("RUN_LABEL")
    if not run_label:
        run_label = _get_required_env("SUITE_ID")

    meta = _resolve_run_metadata_from_env(run_label)

    # REQUIREMENT: always use suite_id for basename (so cdds_<suite_id>)
    workflow_basename = meta["suite_id"]

    # Avoid ConfigParser interpolation problems (e.g. '%' in URLs)
    request = configparser.RawConfigParser()

    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": meta["calendar"],
        "experiment_id": meta.get("experiment_id", "amip") or "amip",
        "institution_id": _get_required_env("INSTITUTION_ID"),
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_id": meta["model_id"],
        "model_type": "AGCM AER",
        "sub_experiment_id": "none",
        "variant_label": meta["variant_label"],
    }

    request["common"] = {
        "external_plugin": "",
        "external_plugin_location": "",
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": _get_required_env("ROOT_PROC_DIR"),
        "root_data_dir": _get_required_env("ROOT_DATA_DIR"),
        "workflow_basename": workflow_basename,
    }

    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_id": meta["suite_id"],
        "model_workflow_revision": "not used except with data request",
        "start_date": f"{start_year}-01-01T00:00:00",
        "streams": "apm",
        "variable_list_file": _get_required_env("VARIABLES_PATH"),
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
    target_path = Path(_get_required_env("REQUEST_PATH"))
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
