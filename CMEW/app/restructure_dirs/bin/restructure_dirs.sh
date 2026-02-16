#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.

# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeuo pipefail

: "${ROOT_DATA_DIR:?ROOT_DATA_DIR must be set}"
: "${CYLC_WORKFLOW_SHARE_DIR:?CYLC_WORKFLOW_SHARE_DIR must be set}"
: "${CDDS_SOFTWARE_DIR:?CDDS_SOFTWARE_DIR must be set}"

RESTRUCTURE_COMMAND="${CDDS_SOFTWARE_DIR}/ceda-mip-tools/bin/restructure_for_cmip6"
ROOT_RESTRUCTURED_DIR="${CYLC_WORKFLOW_SHARE_DIR}/work/"

# This ensures restructuring occurs once after both conversions complete.
echo "[INFO] Restructuring ${ROOT_DATA_DIR} -> ${ROOT_RESTRUCTURED_DIR}"
"${RESTRUCTURE_COMMAND}" -d "${ROOT_RESTRUCTURED_DIR}" "${ROOT_DATA_DIR}"
