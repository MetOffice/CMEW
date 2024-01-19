#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

mkdir -p ${CYLC_WORKFLOW_SHARE_DIR}/etc

echo "Running configure_standardise"
cmew-process-env create_request_file.py
cmew-process-env create_variables_file.py
