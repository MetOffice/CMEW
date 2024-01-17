#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Paths for site-specific environment scripts
SOURCE_PROCESS_PATH="${CYLC_WORKFLOW_RUN_DIR}/site/${SITE}-process-env"
SOURCE_STANDARDISE_PATH="${CYLC_WORKFLOW_RUN_DIR}/site/${SITE}-standardise-env"
# Target directory for installation of the environment scripts
TARGET_DIR="${CYLC_WORKFLOW_SHARE_DIR}/bin"
# Names of the environment scripts
ENV_PROCESS_FILE="cmew-process-env"
ENV_STANDARDISE_FILE="cmew-standardise-env"

# Create the 'bin' directory in the installed workflow.
mkdir "${TARGET_DIR}"

# Copy the environment scripts to the 'bin' directory.
cp "${SOURCE_PROCESS_PATH}" "${TARGET_DIR}/${ENV_PROCESS_FILE}"
cp "${SOURCE_STANDARDISE_PATH}" "${TARGET_DIR}/${ENV_STANDARDISE_FILE}"
