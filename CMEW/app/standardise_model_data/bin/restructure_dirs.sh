#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

CEDA_ROOT_DIR="/home/h03/hadmm/CDDS/github/ceda-mip-tools"
RESTRUCTURE_COMMAND="/bin/restructure_for_cmip6"

ROOT_RESTRUCTURED_DIR="${CYLC_WORKFLOW_SHARE_DIR}/work/"

# For Test model
${CEDA_ROOT_DIR}${RESTRUCTURE_COMMAND} -d ${ROOT_RESTRUCTURED_DIR} ${ROOT_DATA_DIR}

# For Reference model
${CEDA_ROOT_DIR}${RESTRUCTURE_COMMAND} -d ${ROOT_RESTRUCTURED_DIR} ${ROOT_DATA_DIR_REFERENCE}
