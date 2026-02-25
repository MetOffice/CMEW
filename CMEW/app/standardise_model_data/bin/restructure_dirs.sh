#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
BASH_XTRACEFD=1
set -xeuo pipefail

RESTRUCTURE_COMMAND="${CDDS_SOFTWARE_DIR}/ceda-mip-tools/bin/restructure_for_cmip6"

FINAL_WORK_DIR="${CYLC_WORKFLOW_SHARE_DIR}/work"
mkdir -p "${FINAL_WORK_DIR}"

# Stage dir on same filesystem as ROOT_DATA_DIR
STAGE_WORK_DIR="${ROOT_DATA_DIR%/}/../work_stage"
rm -rf "${STAGE_WORK_DIR}"
mkdir -p "${STAGE_WORK_DIR}"

# Restructure (rename ok because same FS: ROOT_DATA_DIR -> STAGE_WORK_DIR)
"${RESTRUCTURE_COMMAND}" -d "${STAGE_WORK_DIR}/" "${ROOT_DATA_DIR}"

# Sync back to cylc-run work (cross-FS safe)
rsync -a "${STAGE_WORK_DIR}/" "${FINAL_WORK_DIR}/"
