#!/bin/bash
# (C) Crown Copyright 2022-2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Install AutoAssess to cylc share/lib directory
pip install $CYLC_WORKFLOW_SHARE_DIR/src/AutoAssess --target="$CYLC_WORKFLOW_SHARE_DIR/lib/python"

# Move executable scripts to share/bin directory
mkdir -p $CYLC_WORKFLOW_SHARE_DIR/bin
mv $CYLC_WORKFLOW_SHARE_DIR/lib/python/bin/* $CYLC_WORKFLOW_SHARE_DIR/bin/
rmdir $CYLC_WORKFLOW_SHARE_DIR/lib/python/bin
