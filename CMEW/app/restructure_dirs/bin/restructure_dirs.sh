#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.

# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -xeuo pipefail

RESTRUCTURE_COMMAND="${CDDS_SOFTWARE_DIR}/ceda-mip-tools/bin/restructure_for_cmip6"
ROOT_RESTRUCTURED_DIR="${CYLC_WORKFLOW_SHARE_DIR}/work/"

# ROOT_DATA_DIR should point to the CDDS data root containing # both REF and TEST run outputs.
"${RESTRUCTURE_COMMAND}" -d "${ROOT_RESTRUCTURED_DIR}" "${ROOT_DATA_DIR}"
