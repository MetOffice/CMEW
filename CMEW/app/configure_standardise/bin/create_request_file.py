#!/usr/bin/env python
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request configuration file from the ESMValTool recipe.

This version supports per-run metadata via an external JSON file pointed
to by RUNS_CONFIG_PATH, while keeping backward compatibility with the
legacy environment variables MODEL_ID/SUITE_ID/CALENDAR/VARIANT_LABEL.

Key behaviour (important for the new "run = suite_id" parameterisation):
- RUN_LABEL may be either:
    * a logical label key in runs.json (e.g. "ref", "eval", "eval2"), OR
    * a suite_id value from runs.json (e.g. "u-bv526", "u-cw673", "u-az513")
  In both cases, the script resolves the correct per-run metadata from
  runs.json.

Expected JSON structure (keys can be snake_case or legacy env-style keys):
{
  "ref":  {"model_id": "...", "suite_id": "...", "calendar": "...",
           "variant_label": "..."},
  "eval": {"model_id": "...", "suite_id": "...", "calendar": "...",
           "variant_label": "..."}
}
"""
import configparser
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def _resolve_runs_config_path() -> Optional[Path]:
    """
    Resolve RUNS_CONFIG_PATH to an absolute Path.

    Supports:
      - absolute paths
      - paths relative to CYLC_WORKFLOW_SHARE_DIR
      - paths relative to workflow source directory,
        e.g. CMEW/etc/runs.json in the repo checkout.
    """
    raw = os.environ.get("RUNS_CONFIG_PATH", "").strip()
    if not raw:
        return None

    # 1) Expand ~ and env vars
    candidate = Path(os.path.expandvars(os.path.expanduser(raw)))

    # 2) If absolute and exists, accept
    if candidate.is_absolute() and candidate.exists():
        return candidate

    # 3) Try relative to CYLC_WORKFLOW_SHARE_DIR (typical runtime)
    share_dir = os.environ.get("CYLC_WORKFLOW_SHARE_DIR", "").strip()
    if share_dir:
        p = Path(share_dir) / candidate
        if p.exists():
            return p

    # 4) Try relative to the workflow source tree:
    #    create_request_file.py usually lives under: CMEW/app/.../bin/
    #    so parents[3] should be CMEW/ (adjust if the layout changes).
    try:
        repo_root = Path(__file__).resolve().parents[3]
        p = repo_root / candidate
        if p.exists():
            return p
    except Exception:
        pass

    # Last resort: return the absolute-resolved path (for error messaging)
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def _load_runs_config_file() -> Dict[str, Any]:
    """Load run mapping from RUNS_CONFIG_PATH JSON file;
    return {} if not configured."""
    path = _resolve_runs_config_path()
    if path is None:
        return {}

    if not path.exists():
        raise FileNotFoundError(
            f"RUNS_CONFIG_PATH points to missing file: {path}"
        )

    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:
        raise RuntimeError(
            f"Failed to read runs config file: {path} ({e})"
        ) from e

    try:
        runs = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Runs config JSON is invalid in {path}: {e}") from e

    if not isinstance(runs, dict):
        raise ValueError(
            f"Runs config in {path} must be a JSON object, got {type(runs)}"
        )

    # Normalize top-level keys to lower-case for matching against RUN_LABEL
    normalized: Dict[str, Any] = {}
    for k, v in runs.items():
        if not isinstance(k, str):
            raise ValueError(
                f"Runs config keys must be strings, got key={k!r}"
            )
        normalized[k.strip().lower()] = v

    return normalized


def _get_required_env(name: str) -> str:
    """Fetch env var or raise a KeyError with a clear message."""
    val = os.environ.get(name, "").strip()
    if not val:
        raise KeyError(f"{name} must be set")
    return val


def _normalize_run_entry(run_key: str, cfg: Any) -> Dict[str, str]:
    """Validate and normalize a single run entry object from runs.json."""
    if not isinstance(cfg, dict):
        raise ValueError(
            f"Runs config entry for '{run_key}' must be an object,\
                got {type(cfg)}"
        )

    # Support both snake_case and legacy env-style keys
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
      1) RUNS_CONFIG_PATH JSON file (preferred)
      2) Legacy env vars MODEL_ID/SUITE_ID/CALENDAR/VARIANT_LABEL (fallback)

    Important: with "run = suite_id" parameterisation, RUN_LABEL will often be
    a suite_id (e.g. 'u-bv526'). In that case we search runs.json values for a
    matching suite_id.
    """
    runs_cfg = _load_runs_config_file()

    if runs_cfg:
        # Case A: RUN_LABEL matches a top-level key (ref/eval/eval2)
        if run_label in runs_cfg:
            return _normalize_run_entry(run_label, runs_cfg[run_label])

        # Case B: RUN_LABEL is a suite_id (u-xxxxx) - search entries
        for key, cfg in runs_cfg.items():
            if not isinstance(cfg, dict):
                continue
            suite_id = cfg.get("suite_id") or cfg.get("SUITE_ID")
            if isinstance(suite_id, str) and suite_id.strip() == run_label:
                return _normalize_run_entry(key, cfg)

        raise KeyError(
            f"RUN_LABEL='{run_label}' not found as a key in runs config"
            f"and did not match any suite_id."
            f"Available keys: {sorted(runs_cfg.keys())}"
        )

    # Backward-compatible mode (no runs.json configured)
    return {
        "model_id": _get_required_env("MODEL_ID"),
        "suite_id": _get_required_env("SUITE_ID"),
        "calendar": _get_required_env("CALENDAR"),
        "variant_label": _get_required_env("VARIANT_LABEL"),
    }


def create_request() -> configparser.ConfigParser:
    """Retrieve CDDS request information from Rose suite configuration."""
    start_year = int(_get_required_env("START_YEAR"))
    number_of_years = int(_get_required_env("NUMBER_OF_YEARS"))
    end_year = start_year + number_of_years

    run_label = os.environ.get("RUN_LABEL", "").strip().lower()
    if not run_label:
        raise KeyError(
            "RUN_LABEL must be set (e.g. 'ref' or 'eval' or a suite_id)"
        )

    meta = _resolve_run_metadata(run_label)

    # Use parent CMEW run name if available to avoid cross-run collisions
    # parent_run = os.environ.get("CYLC_WORKFLOW_RUN_NAME", "").strip() \
    #        or "run"
    # workflow_prefix = (
    #     os.environ.get("CDDS_WORKFLOW_BASENAME_PREFIX", "CMEW").strip()
    #     or "CMEW"
    # )

    # Safe, deterministic child name
    # NOTE: run_label may be suite_id now; that's OK and is actually desirable
    # if you want uniqueness per suite.
    # workflow_basename = f"{workflow_prefix}_{parent_run}_{run_label}"

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
        "mip_table_dir": os.path.expanduser(
            "~cdds/etc/mip_tables/GCModelDev/0.0.25"
        ),
        "mode": "relaxed",
        "package": "round-1",
        "root_proc_dir": _get_required_env("ROOT_PROC_DIR"),
        "root_data_dir": _get_required_env("ROOT_DATA_DIR"),
        "workflow_basename": os.environ["SUITE_ID"],
    }

    request["data"] = {
        "end_date": f"{end_year}-01-01T00:00:00",
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        # IMPORTANT: use per-run suite id (not the legacy env var)
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
    """Write the request configuration to a file at ``target_path``."""
    with open(target_path, mode="w", encoding="utf-8") as file_handle:
        request.write(file_handle)


def main() -> None:
    target_path = Path(_get_required_env("REQUEST_PATH"))
    request = create_request()
    write_request(request, target_path)


if __name__ == "__main__":
    main()
