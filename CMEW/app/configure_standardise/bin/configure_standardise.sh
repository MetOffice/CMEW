#!/bin/bash
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

echo "Running configure_standardise"

# Create request configuration file and variables file.
cmew-esmvaltool-env create_request_file.py
cmew-esmvaltool-env create_variables_file.py

# Create CDDS directory structure and variables list.
cmew-standardise-env create_cdds_directory_structure "${REQUEST_PATH}"
cmew-standardise-env prepare_generate_variable_list "${REQUEST_PATH}"
