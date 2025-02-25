#!/bin/bash
# (C) Crown Copyright 2022-2025, Met Office.
# The LICENSE.md file contains full licensing details.
#
# USAGE compare.sh
#
# ENVIRONMENT
#   OUTPUT_DIR    The full path to the output directory for the 'process' task
#   METRIC_DIR    The name of the directory in OUTPUT_DIR containing the
#                 METRIC_FILES
#   METRIC_FILES  The files expected to be produced by the process task for the
#                 metric

# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

# Ensure the files produced by the 'process' task for the metric match the
# expected files.
for metric_file in ${METRIC_FILES}
    do
        OUTPUT_METRIC_PATH="${OUTPUT_DIR}/${METRIC_DIR}*/${metric_file}"
        if [ ! -f ${OUTPUT_METRIC_PATH} ]; then
            echo "${OUTPUT_METRIC_PATH} does not exist"
            exit 1
        fi
    done
