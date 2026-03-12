#!/bin/bash
# (C) Crown Copyright 2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and EVAL runs via CDDS.

BASH_XTRACEFD=1
set -eux

cmew-standardise-env cdds_convert "${REQUEST_PATH}"
