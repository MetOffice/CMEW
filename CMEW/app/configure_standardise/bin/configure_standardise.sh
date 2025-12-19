#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -euo pipefail
set -x


echo "Running configure_standardise (two runs: REF and TEST)"

# Helper function to configure one run (REF or TEST)
configure_run() {
    local RUN_PREFIX="$1"           # "REF" or "TEST"
    local REQUEST_PATH_VAR="$2"     # e.g. "REQUEST_PATH_REF"
    local VARIABLES_PATH_VAR="$3"   # e.g. "VARIABLES_PATH_REF"

    # Indirect expansion to read env vars like REF_MODEL_ID, TEST_MODEL_ID, etc.
    local MODEL_ID_VAR="${RUN_PREFIX}_MODEL_ID"
    local SUITE_ID_VAR="${RUN_PREFIX}_SUITE_ID"
    local CALENDAR_VAR="${RUN_PREFIX}_CALENDAR"
    local VARIANT_VAR="${RUN_PREFIX}_VARIANT_LABEL"

    local MODEL_ID_VALUE="${!MODEL_ID_VAR}"
    local SUITE_ID_VALUE="${!SUITE_ID_VAR}"
    local CALENDAR_VALUE="${!CALENDAR_VAR}"
    local VARIANT_VALUE="${!VARIANT_VAR}"

    # Per-run request & variables paths
    local REQUEST_PATH_VALUE="${!REQUEST_PATH_VAR}"
    local VARIABLES_PATH_VALUE="${!VARIABLES_PATH_VAR}"

    echo "[INFO] Configuring run ${RUN_PREFIX}:"
    echo "       MODEL_ID=${MODEL_ID_VALUE}"
    echo "       SUITE_ID=${SUITE_ID_VALUE}"
    echo "       CALENDAR=${CALENDAR_VALUE}"
    echo "       VARIANT_LABEL=${VARIANT_VALUE}"
    echo "       REQUEST_PATH=${REQUEST_PATH_VALUE}"
    echo "       VARIABLES_PATH=${VARIABLES_PATH_VALUE}"

    # Export values expected by the Python scripts
    export MODEL_ID="${MODEL_ID_VALUE}"
    export SUITE_ID="${SUITE_ID_VALUE}"
    export CALENDAR="${CALENDAR_VALUE}"
    export VARIANT_LABEL="${VARIANT_VALUE}"

    # Also export the generic names used inside the scripts
    export REQUEST_PATH="${REQUEST_PATH_VALUE}"
    export VARIABLES_PATH="${VARIABLES_PATH_VALUE}"

    # Create request configuration file and variables file for this run.
    cmew-esmvaltool-env create_request_file.py
    cmew-esmvaltool-env create_variables_file.py

    # Create CDDS directory structure and variables list for this run.
    cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}"
    cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}"
}

# Configure reference run (REF_*)
configure_run "REF"  "REQUEST_PATH_REF"  "VARIABLES_PATH_REF"

# Configure test run (TEST_*)
configure_run "TEST" "REQUEST_PATH_TEST" "VARIABLES_PATH_TEST"

echo "[INFO] configure_standardise completed for REF and TEST runs"
