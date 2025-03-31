#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

echo "Running configure_standardise"

# For Test model
cmew-process-env create_request_file.py --path "${REQUEST_PATH}" /
    --model_id "${MODEL_ID}" --suite_id "${SUITE_ID}" /
    --calendar "${CALENDAR}" --variant "${VARIANT_LABEL}"

# For Reference model
cmew-process-env create_request_file.py --path "${REQUEST_PATH_REFERENCE}" /
    --model_id "${MODEL_ID_REFERENCE}" --suite_id "${SUITE_ID_REFERENCE}" /
    --calendar "${CALENDAR_REFERENCE}" --variant "${VARIANT_LABEL_REFERENCE}"

# For both test & reference models
cmew-process-env create_variables_file.py

# Running setup commands for CDDS

# For Test model
cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}"

# For Reference model
cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH_REFERENCE}" -c "${ROOT_PROC_DIR_REFERENCE}" -t "${ROOT_DATA_DIR_REFERENCE}"

# For Test model
cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}" -c "${ROOT_PROC_DIR}" -t "${ROOT_DATA_DIR}" --use_proc_dir -r "${VARIABLES_PATH}"

# For Reference model
cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH_REFERENCE}" -c "${ROOT_PROC_DIR_REFERENCE}" -t "${ROOT_DATA_DIR_REFERENCE}" --use_proc_dir -r "${VARIABLES_PATH}"
