#!/bin/bash
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Clone the ESMValTool branch.
# The quiet ('-q') option to prevent the progress status from being reported.
git clone -q -b "${ESMVALTOOL_BRANCH}" "${ESMVALTOOL_URL}" "${ESMVALTOOL_DIR}"
