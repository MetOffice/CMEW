#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

CEDA_ROOT_DIR="/home/h03/hadmm/CDDS/github/ceda-mip-tools"
RESTRUCTURE_COMMAND="/bin/restructure_for_cmip6"

CDDS_DATA_DIR="${CYLC_WORKFLOW_SHARE_DIR}/data/cdds/cdds_data/"
RESTRUCTURED_DIR="${CYLC_WORKFLOW_SHARE_DIR}/work/"

${CEDA_ROOT_DIR}${RESTRUCTURE_COMMAND} -d ${RESTRUCTURED_DIR} ${CDDS_DATA_DIR}

# ESMValTool reads from ./GCModelDev/CMIP/ so need to rename the directory.
mv "${RESTRUCTURED_DIR}/GCModelDev/ESMVal/" "${RESTRUCTURED_DIR}/GCModelDev/CMIP/"
