#!/bin/bash
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

pip install "$SOURCE_DIR" --target="$TARGET_DIR"

# Move executable scripts from $TARGET_DIR to $SCRIPT_DIR.
mv $TARGET_DIR/bin/* $SCRIPT_DIR/.
rmdir $TARGET_DIR/bin
