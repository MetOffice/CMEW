#!/bin/bash
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Clone the Aerosol Toolkit to lib/python directory
git clone -q -b "main" "git@github.com:MetOffice/aerosol_evaluation_toolkit.git" "${AEROSOL_TOOLKIT_DIR}"

