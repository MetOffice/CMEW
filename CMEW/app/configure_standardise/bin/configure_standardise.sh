#!/bin/bash
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeuo pipefail

# ---------------------------------------------------------------------------
# 0. Defensive programming
# ---------------------------------------------------------------------------
: "${RUN_LABEL:?RUN_LABEL must be set (e.g. ref/eval)}"
: "${REQUEST_PATH:?REQUEST_PATH must be set}"
: "${MODEL_ID:?MODEL_ID must be set}"
: "${SUITE_ID:?SUITE_ID must be set}"
: "${CALENDAR:?CALENDAR must be set}"
: "${VARIABLES_PATH:?VARIABLES_PATH must be set}"

echo "[INFO] RUN_LABEL=${RUN_LABEL}"
echo "[INFO] MODEL_ID=${MODEL_ID}"
echo "[INFO] SUITE_ID=${SUITE_ID}"
echo "[INFO] CALENDAR=${CALENDAR}"
echo "[INFO] VARIANT_LABEL=${VARIANT_LABEL}"

echo "[INFO] Running configure_standardise for RUN_LABEL=${RUN_LABEL}"
echo "[INFO] REQUEST_PATH=${REQUEST_PATH}"

test -f "${VARIABLES_PATH}" || { echo "[ERROR] variables file missing: ${VARIABLES_PATH}" >&2; exit 2; }

cmew-esmvaltool-env create_request_file.py
cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}"
cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}"
