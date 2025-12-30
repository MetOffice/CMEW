#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeuo pipefail

echo "[INFO] Running configure_standardise for REF and EVAL runs"

# ---------------------------------------------------------------------------
# 0. Defensive programming
# ---------------------------------------------------------------------------
: "${REQUEST_PATH_REF:?REQUEST_PATH_REF must be set}"
: "${REQUEST_PATH_EVAL:?REQUEST_PATH_EVAL must be set}"

echo "[INFO] Using REQUEST_PATH_REF=${REQUEST_PATH_REF}"
echo "[INFO] Using REQUEST_PATH_EVAL=${REQUEST_PATH_EVAL}"

# Require REF_* and base MODEL_* metadata in the environment
: "${REF_MODEL_ID:?REF_MODEL_ID must be set}"
: "${REF_SUITE_ID:?REF_SUITE_ID must be set}"
: "${REF_CALENDAR:?REF_CALENDAR must be set}"
: "${MODEL_ID:?MODEL_ID (evaluation) must be set}"
: "${SUITE_ID:?SUITE_ID (evaluation) must be set}"
: "${CALENDAR:?CALENDAR (evaluation) must be set}"

# ---------------------------------------------------------------------------
# 1. Create variables.txt once (shared by both runs)
# ---------------------------------------------------------------------------
echo "[INFO] Creating variables file from ESMValTool recipe"
cmew-esmvaltool-env create_variables_file.py

# ---------------------------------------------------------------------------
# 2. Helper: configure CDDS request + directory structure for a given run
# ---------------------------------------------------------------------------
create_for_run() {
    local RUN_LABEL="$1"

    local run_model_id=""
    local run_suite_id=""
    local run_calendar=""
    local run_variant=""
    local run_request=""

    case "${RUN_LABEL}" in
        REF)
            run_model_id="${REF_MODEL_ID}"
            run_suite_id="${REF_SUITE_ID}"
            run_calendar="${REF_CALENDAR}"
            run_variant="${REF_VARIANT_LABEL:-}"
            run_request="${REQUEST_PATH_REF}"
            ;;
        EVAL)
            # Evaluation run uses the base MODEL_ID/SUITE_ID/CALENDAR/VARIANT_LABEL
            run_model_id="${MODEL_ID}"
            run_suite_id="${SUITE_ID}"
            run_calendar="${CALENDAR}"
            run_variant="${VARIANT_LABEL:-}"
            run_request="${REQUEST_PATH_EVAL}"
            ;;
        *)
            echo "[ERROR] Unknown run label: ${RUN_LABEL}" >&2
            exit 1
            ;;
    esac

    (
        # Subshell: don't leak these exports back out into the caller.
        export MODEL_ID="${run_model_id}"
        export SUITE_ID="${run_suite_id}"
        export CALENDAR="${run_calendar}"
        export VARIANT_LABEL="${run_variant}"
        export REQUEST_PATH="${run_request}"

        echo "[INFO] Creating request for ${RUN_LABEL} run at: ${REQUEST_PATH}"
        cmew-esmvaltool-env create_request_file.py

        echo "[INFO] Creating CDDS directory structure for ${RUN_LABEL} run"
        cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}"
        cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}"
    )
}

# ---------------------------------------------------------------------------
# 3. Configure both runs
# ---------------------------------------------------------------------------
create_for_run REF
create_for_run EVAL

echo "[INFO] configure_standardise completed for REF and EVAL runs"
