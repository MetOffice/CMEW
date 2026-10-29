#!/bin/bash
# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

COMMAND=${CDDS_SOFTWARE_DIR}/ceda-mip-tools/bin/restructure_for_cmip6

${COMMAND} -d "${ROOT_REORGANISED_DIR}" "${ROOT_DATA_DIR}"
