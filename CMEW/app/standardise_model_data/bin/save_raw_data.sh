#!/bin/bash
# (C) Crown Copyright 2025-2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and EVAL runs via CDDS.

BASH_XTRACEFD=1
set -xeu

# If RAW_DATA_DIR is configured, copy extracted raw data only when the target
# directory, ${RAW_DATA_DIR}/${dataset}, is empty.
# If it is not empty, emit a log.err message and do not copy.
dataset="${CYLC_TASK_PARAM_dataset}"
if [[ -n "${RAW_DATA_DIR:-}" ]]; then
    RAW_DATA_DIR_SUITE="${RAW_DATA_DIR}"/"${dataset}"
    mkdir -p "${RAW_DATA_DIR_SUITE}"

    shopt -s nullglob dotglob
    raw_dir_contents=("${RAW_DATA_DIR_SUITE}"/*)
    shopt -u nullglob dotglob

    if (( ${#raw_dir_contents[@]} > 0 )); then
        echo "log.err: raw data dir was not empty: ${RAW_DATA_DIR_SUITE}" >&2
        exit 1
    fi

    echo "[INFO] RAW_DATA_DIR_SUITE is empty, locating suite input directories"

    set +x
    src_dir="$(find "${ROOT_DATA_DIR}" -type d -path "*/input/${dataset}" -print -quit)"
    set -x

    if [[ -z "${src_dir}" ]]; then
        echo "log.err: Could not find suite input directory for ${dataset} under ${ROOT_DATA_DIR}" >&2
        exit 1
    fi

    echo "[INFO] Copying ${dataset} raw data: ${src_dir}"
    cp -a "${src_dir}"/* "${RAW_DATA_DIR_SUITE}/"

    echo "[INFO] Raw suite input directories copied to ${RAW_DATA_DIR_SUITE}"
else
    echo "[INFO] RAW_DATA_DIR is not set, skipping raw data copy"
fi
