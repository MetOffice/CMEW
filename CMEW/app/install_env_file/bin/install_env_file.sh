#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Paths for site-specific environments scripts
SOURCE_PATH="${CYLC_WORKFLOW_RUN_DIR}/site/${SITE}-process-env"
SOURCE_STANDARDISE_PATH="${CYLC_WORKFLOW_RUN_DIR}/site/${SITE}-standardise-env"
# Target directory for installation of the environments scripts
TARGET_DIR="${CYLC_WORKFLOW_RUN_DIR}/share/bin"
# Names of the environments scripts
ENV_FILE="cmew-env"
ENV_STANDARDISE_FILE="cmew-standardise-env"

# Create the 'bin' directory in the installed workflow.
mkdir "${TARGET_DIR}"

# Copy the environments scripts to the 'bin' directory.
cp "${SOURCE_PATH}" "${TARGET_DIR}/${ENV_FILE}"
cp "${SOURCE_STANDARDISE_PATH}" "${TARGET_DIR}/${ENV_STANDARDISE_FILE}"
