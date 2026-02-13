#!/bin/bash
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and EVAL runs via CDDS.

BASH_XTRACEFD=1
set -xeuo pipefail

: "${RUN_LABEL:?RUN_LABEL must be set (ref/eval)}"
: "${REQUEST_PATH:?REQUEST_PATH must be set}"

echo "[INFO] Running standardise_model_data for RUN_LABEL=${RUN_LABEL}"
echo "[INFO] Using request: ${REQUEST_PATH}"

cmew-standardise-env cdds_convert "${REQUEST_PATH}"

echo "[INFO] standardise_model_data completed for ${RUN_LABEL}"
