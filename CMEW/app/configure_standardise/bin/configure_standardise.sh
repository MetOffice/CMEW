#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

mkdir -p ${CYLC_WORKFLOW_SHARE_DIR}/etc

echo "Running configure_standardise"
echo "Get request.json file"

cmew-process-env create_variables_file.py

# Running setup commands for CDDS

export WORKING_DIRECTORY="${CYLC_WORKFLOW_SHARE_DIR}/data/cdds"
export ROOT_PROC_DIR="${WORKING_DIRECTORY}/proc"
export ROOT_DATA_DIR="${WORKING_DIRECTORY}/cdds_data"

mkdir -p ${ROOT_PROC_DIR}
mkdir -p ${ROOT_DATA_DIR}

cmew-standardise-env create_cdds_directory_structure "${CYLC_WORKFLOW_SHARE_DIR}/etc/request.json" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}"

cmew-standardise-env prepare_generate_variable_list "${CYLC_WORKFLOW_SHARE_DIR}/etc/request.json" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}" --use_proc_dir -r "${CYLC_WORKFLOW_SHARE_DIR}/etc/variables.txt"
