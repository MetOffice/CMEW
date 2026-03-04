#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeuo pipefail

# ---------------------------------------------------------------------------
# 0. Defensive programming (multi-run)
# ---------------------------------------------------------------------------
: "${RUN_LABEL:?RUN_LABEL must be set (suite_id e.g. u-bv526)}"
: "${REQUEST_PATH:?REQUEST_PATH must be set}"
: "${VARIABLES_PATH:?VARIABLES_PATH must be set}"

: "${START_YEAR:?START_YEAR must be set}"
: "${NUMBER_OF_YEARS:?NUMBER_OF_YEARS must be set}"
: "${INSTITUTION_ID:?INSTITUTION_ID must be set}"
: "${ROOT_PROC_DIR:?ROOT_PROC_DIR must be set}"
: "${ROOT_DATA_DIR:?ROOT_DATA_DIR must be set}"

# We support two-model metadata via REF_* + non-REF vars.
# Decide which set must be present based on RUN_LABEL.
REF_SUITE_ID="${REF_SUITE_ID:-}"
SUITE_ID="${SUITE_ID:-}"

echo "[INFO] RUN_LABEL=${RUN_LABEL}"
echo "[INFO] REQUEST_PATH=${REQUEST_PATH}"
echo "[INFO] VARIABLES_PATH=${VARIABLES_PATH}"
echo "[INFO] START_YEAR=${START_YEAR}"
echo "[INFO] NUMBER_OF_YEARS=${NUMBER_OF_YEARS}"
echo "[INFO] INSTITUTION_ID=${INSTITUTION_ID}"
echo "[INFO] ROOT_PROC_DIR=${ROOT_PROC_DIR}"
echo "[INFO] ROOT_DATA_DIR=${ROOT_DATA_DIR}"

if [[ -n "${REF_SUITE_ID}" && "${RUN_LABEL}" == "${REF_SUITE_ID}" ]]; then
  : "${REF_MODEL_ID:?REF_MODEL_ID must be set (because RUN_LABEL == REF_SUITE_ID)}"
  : "${REF_SUITE_ID:?REF_SUITE_ID must be set (because RUN_LABEL == REF_SUITE_ID)}"
  : "${REF_CALENDAR:?REF_CALENDAR must be set (because RUN_LABEL == REF_SUITE_ID)}"
  : "${REF_VARIANT_LABEL:?REF_VARIANT_LABEL must be set (because RUN_LABEL == REF_SUITE_ID)}"

  echo "[INFO] Mode: REF (matched RUN_LABEL==REF_SUITE_ID)"
  echo "[INFO] REF_MODEL_ID=${REF_MODEL_ID}"
  echo "[INFO] REF_SUITE_ID=${REF_SUITE_ID}"
  echo "[INFO] REF_CALENDAR=${REF_CALENDAR}"
  echo "[INFO] REF_VARIANT_LABEL=${REF_VARIANT_LABEL}"
else
  # evaluation / default path
  : "${MODEL_ID:?MODEL_ID must be set}"
  : "${SUITE_ID:?SUITE_ID must be set}"
  : "${CALENDAR:?CALENDAR must be set}"
  : "${VARIANT_LABEL:?VARIANT_LABEL must be set}"

  echo "[INFO] Mode: non-REF (legacy/eval/default)"
  echo "[INFO] MODEL_ID=${MODEL_ID}"
  echo "[INFO] SUITE_ID=${SUITE_ID}"
  echo "[INFO] CALENDAR=${CALENDAR}"
  echo "[INFO] VARIANT_LABEL=${VARIANT_LABEL}"
fi

# ---------------------------------------------------------------------------
# 1. Create variables.txt once (shared by both runs)
# ---------------------------------------------------------------------------
echo "[INFO] Creating variables file from ESMValTool recipe"
cmew-esmvaltool-env create_variables_file.py

echo "[INFO] Running configure_standardise for RUN_LABEL=${RUN_LABEL}"

test -f "${VARIABLES_PATH}" || {
  echo "[ERROR] variables file missing: ${VARIABLES_PATH}" >&2
  exit 2
}

# ---------------------------------------------------------------------------
# 2. Create request and configure CDDS conversion workflow
# ---------------------------------------------------------------------------
cmew-esmvaltool-env create_request_file.py
cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}"
cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}"
