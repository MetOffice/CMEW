#!/bin/bash
# (C) Crown Copyright 2025-2026, Met Office.
# The LICENSE.md file contains full licensing details.

BASH_XTRACEFD=1
set -xeuo pipefail

echo "[INFO] Running standardise_model_data for REF and EVAL runs"

# Determine where to put raw extracted data
# If RAW_DATA_DIR is set and non-empty, use it, otherwise default to task work dir.
RAW_ROOT="${RAW_DATA_DIR:-${CYLC_TASK_WORK_DIR:-${PWD}}}"
echo "[INFO] Using RAW_ROOT='${RAW_ROOT}' for raw CDDS output"

# Point CDDS raw output at RAW_ROOT, leaving ROOT_DATA_DIR for standardised layout.
# CDDS will create subdirectories under these roots per request configuration.[web:1]
export CDDS_PROC_DIR="${RAW_ROOT}/proc"
export CDDS_DATA_DIR="${RAW_ROOT}/data"

mkdir -p "${CDDS_PROC_DIR}" "${CDDS_DATA_DIR}"

# Expect these to be set from flow.cylc runtime environment:
# REQUEST_PATH_REF
# REQUEST_PATH_EVAL

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
