#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeu

# We support two-model metadata via REF_* + non-REF vars.
# Decide which set must be present based on RUN_LABEL.
REF_SUITE_ID="${REF_SUITE_ID:-}"
SUITE_ID="${SUITE_ID:-}"

# ---------------------------------------------------------------------------
# 1. Create variables.txt
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
