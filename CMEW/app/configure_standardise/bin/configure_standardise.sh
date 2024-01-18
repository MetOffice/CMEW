#!/bin/bash
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

echo "Running configure_standardise"
echo "Get request.json file"
cmew-process-env configure_standardise.py
echo "Get variable list"
