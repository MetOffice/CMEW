#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

echo "Running configure_standardise"

echo "Get request.json file"
# The directory of the hardcoded request.json file
SOURCE_PATH="${CYLC_WORKFLOW_RUN_DIR}/app/configure_standardise/mock_data"
TARGET_DIR="${CYLC_WORKFLOW_SHARE_DIR}/etc"
# Copy the request.json file to the 'share/etc' directory
mkdir -p ${TARGET_DIR}
cp "${SOURCE_PATH}/request.json" "${TARGET_DIR}/request.json"

echo "Get variable list"
