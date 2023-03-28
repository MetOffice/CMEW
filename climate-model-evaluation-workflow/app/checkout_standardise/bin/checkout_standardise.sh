#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Remove CDDS directory if it exists
if [[ -d ${CDDS_DIR} ]]; then
    rm -rf "${CDDS_DIR}"
fi

# Checkout the specified branch of the CMEW using -q
