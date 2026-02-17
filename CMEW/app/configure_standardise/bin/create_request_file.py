#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.

"""
Generates the request configuration file from the ESMValTool recipe.

Supports per-run metadata via RUNS_CONFIG_PATH + RUN_LABEL, while keeping
backward compatibility with legacy env vars MODEL_ID/SUITE_ID/
CALENDAR/VARIANT_LABEL.

Naming requirement:
- In ALL modes (legacy and multi-run), set workflow_basename = suite_id
  so CDDS paths are cdds_<suite_id>.
- MIP_TABLE_DIR must be set and written to common.mip_table_dir.
  This must match ESMValTool developer config custom.cmor_path.
"""

import configparser
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def _resolve_runs_config_path() -> Optional[Path]:
    raw = os.environ.get("RUNS_CONFIG_PATH", "").strip()
    if not raw:
        return None

    candidate = Path(os.path.expandvars(os.path.expanduser(raw)))

    if candidate.is_absolute() and candidate.exists():
        return candidate

    share_dir = os.environ.get("CYLC_WORKFLOW_SHARE_DIR", "").strip()
    if share_dir:
        p = Path(share_dir) / candidate
        if p.exists():
            return p

    try:
        repo_root = Path(__file__).resolve().parents[3]
        p = repo_root / candidate
        if p.exists():
            return p
    except Exception:
        pass

    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def _load_runs_config_file() -> Dict[str, Any]:
    path = _resolve_runs_config_path()
    if path is None:
        return {}

    if not path.exists():
        raise FileNotFoundError(
            f"RUNS_CONFIG_PATH points to missing file: {path}"
        )

    raw = path.read_text(encoding="utf-8")
    runs = json.loads(raw)

    if not isinstance(runs, dict):
        raise ValueError(
            f"Runs config in {path} must be a JSON object, got {type(runs)}"
        )

    normalized: Dict[str, Any] = {}
    for k, v in runs.items():
        if not isinstance(k, str):
            raise ValueError(
                f"Runs config keys must be strings, got key={k!r}"
            )
        normalized[k.strip().lower()] = v

    return normalized


def _get_required_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise KeyError(f"{name} must be set")
    return val


def _get_required_mip_table_dir() -> str:
    """
    Return expanded MIP_TABLE_DIR.

    Must match ESMValTool developer config custom.cmor_path.
    """
    mip_table_dir = os.environ.get("MIP_TABLE_DIR", "").strip()
    if not mip_table_dir:
        raise KeyError(
            "MIP_TABLE_DIR must be set (must match ESMValTool developer "
            "config custom.cmor_path)."
        )
    return os.path.expanduser(mip_table_dir)


def _normalize_run_entry(run_key: str, cfg: Any) -> Dict[str, str]:
    if not isinstance(cfg, dict):
        raise ValueError(
            f"Runs config entry for '{run_key}' must be an object, "
            f"got {type(cfg)}"
        )

    model_id = cfg.get("model_id") or cfg.get("MODEL_ID")
    suite_id = cfg.get("suite_id") or cfg.get("SUITE_ID")
    calendar = cfg.get("calendar") or cfg.get("CALENDAR")
    variant_label = cfg.get("variant_label") or cfg.get("VARIANT_LABEL")

    missing = [
        k
        for k, v in {
            "model_id": model_id,
            "suite_id": suite_id,
            "calendar": calendar,
            "variant_label": variant_label,
        }.items()
        if not (isinstance(v, str) and v.strip())
    ]
    if missing:
        raise KeyError(
            f"Missing keys for run '{run_key}' in runs config: {missing}"
        )

    return {
        "model_id": str(model_id).strip(),
        "suite_id": str(suite_id).strip(),
        "calendar": str(calendar).strip(),
        "variant_label": str(variant_label).strip(),
    }


def _resolve_run_metadata(run_label: str) -> Dict[str, str]:
    """
    Resolve per-run metadata in priority order:
      1) runs.json (RUNS_CONFIG_PATH) if configured
      2) Legacy env vars (MODEL_ID/SUITE_ID/CALENDAR/VARIANT_LABEL)

    RUN_LABEL may be:
      - a key in runs.json ("ref", "eval", ...)
      - a suite_id value ("u-xxxxx") in runs.json entries
    """
    runs_cfg = _load_runs_config_file()

    if runs_cfg:
        if run_label in runs_cfg:
            return _normalize_run_entry(run_label, runs_cfg[run_label])

        for key, cfg in runs_cfg.items():
            if not isinstance(cfg, dict):
                continue
            suite_id = cfg.get("suite_id") or cfg.get("SUITE_ID")
            if isinstance(suite_id, str) and suite_id.strip() == run_label:
                return _normalize_run_entry(key, cfg)

        raise KeyError(
            f"RUN_LABEL='{run_label}' not found as a key in runs config "
            f"and did not match any suite_id. Available keys: "
            f"{sorted(runs_cfg.keys())}"
        )

    # Legacy fallback
    return {
        "model_id": _get_required_env("MODEL_ID"),
        "suite_id": _get_required_env("SUITE_ID"),
        "calendar": _get_required_env("CALENDAR"),
        "variant_label": _get_required_env("VARIANT_LABEL"),
    }


def create_request() -> configparser.ConfigParser:
    # required and must match ESMValTool developer config custom.cmor_path
    mip_table_dir = _get_required_mip_table_dir()

    start_year = int(_get_required_env("START_YEAR"))
    number_of_years = int(_get_required_env("NUMBER_OF_YEARS"))
    end_year = start_year + number_of_years

    run_label = os.environ.get("RUN_LABEL", "").strip().lower()

    if run_label:
        meta = _resolve_run_metadata(run_label)
    else:
        # Legacy mode: do NOT require RUN_LABEL (unit tests rely on this)
        meta = {
            "model_id": _get_required_env("MODEL_ID"),
            "suite_id": _get_required_env("SUITE_ID"),
            "calendar": _get_required_env("CALENDAR"),
            "variant_label": _get_required_env("VARIANT_LABEL"),
        }

    # REQUIREMENT: always use suite_id for basename
    workflow_basename = meta["suite_id"]

    request = configparser.ConfigParser()

    request["metadata"] = {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "calendar": meta["calendar"],
        "experiment_id": "amip",
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
        "mip_table_dir": mip_table_dir,
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
    with open(target_path, mode="w", encoding="utf-8") as file_handle:
        request.write(file_handle)


def main() -> None:
    target_path = Path(_get_required_env("REQUEST_PATH"))
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
