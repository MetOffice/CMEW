#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and TEST runs via CDDS.

BASH_XTRACEFD=1
set -euo pipefail
set -x

echo "[INFO] Running standardise_model_data for REF and TEST runs"

# Expect these to be set from flow.cylc runtime environment:
#   REQUEST_PATH_REF
#   REQUEST_PATH_TEST

# Run CDDS convert for reference run
echo "[INFO] Running cdds_convert for REF run with request:
${REQUEST_PATH_REF}"
cmew-standardise-env cdds_convert "${REQUEST_PATH_REF}"

# Run CDDS convert for test run
echo "[INFO] Running cdds_convert for TEST run with request:
${REQUEST_PATH_TEST}"
cmew-standardise-env cdds_convert "${REQUEST_PATH_TEST}"

# Restructure all data under ROOT_DATA_DIR into CMIP6-like layout.
# restructure_dirs.sh already uses ROOT_DATA_DIR from the environment.
echo "[INFO] Restructuring CMIP6 directories for all runs"
cmew-standardise-env restructure_dirs.sh

echo "[INFO] standardise_model_data completed for REF and TEST runs"
