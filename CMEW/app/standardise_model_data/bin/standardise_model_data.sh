#!/bin/bash
# (C) Crown Copyright 2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and EVAL runs via CDDS.

BASH_XTRACEFD=1
set -xeuo pipefail

echo "[INFO] Running standardise_model_data for REF and EVAL runs"

# Expect these to be set from flow.cylc runtime environment:
#   REQUEST_PATH_REF
#   REQUEST_PATH_EVAL

echo "[INFO] Running cdds_convert for REF run using: ${REQUEST_PATH_REF}"
cmew-standardise-env cdds_convert "${REQUEST_PATH_REF}"

echo "[INFO] Running cdds_convert for EVAL run using: ${REQUEST_PATH_EVAL}"
cmew-standardise-env cdds_convert "${REQUEST_PATH_EVAL}"

# Restructure all data under ROOT_DATA_DIR into CMIP6-like layout.
# restructure_dirs.sh already uses ROOT_DATA_DIR from the environment.
echo "[INFO] Running restructure_dirs.sh over ROOT_DATA_DIR=${ROOT_DATA_DIR}"
echo "[INFO] Restructuring CMIP6 directories for all runs"
cmew-standardise-env restructure_dirs.sh

echo "[INFO] standardise_model_data completed for REF and EVAL runs"
