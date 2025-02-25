#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

echo "Running configure_standardise"

cmew-process-env create_request_file.py

cmew-process-env create_variables_file.py

# Running setup commands for CDDS

cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}"

cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}" --use_proc_dir -r "${VARIABLES_PATH}"
