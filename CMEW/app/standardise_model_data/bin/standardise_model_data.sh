#!/bin/bash
# (C) Crown Copyright 2025, Met Office.
# The LICENSE.md file contains full licensing details.
# Standardise data for both REF and EVAL runs via CDDS.

BASH_XTRACEFD=1
set -eux

cmew-standardise-env cdds_convert "${REQUEST_PATH}"

# If RAW_DATA_DIR is configured, copy extracted raw data only when the target
# directory is empty. If it is not empty, emit a log.err message and do not copy.
if [[ -n "${RAW_DATA_DIR:-}" ]]; then
    mkdir -p "${RAW_DATA_DIR}"

    shopt -s nullglob dotglob
    raw_dir_contents=("${RAW_DATA_DIR}"/*)
    shopt -u nullglob dotglob

    if (( ${#raw_dir_contents[@]} > 0 )); then
        echo "log.err: RAW_DATA_DIR was not empty: ${RAW_DATA_DIR}" >&2
        exit 1
    fi

    echo "[INFO] RAW_DATA_DIR is empty, locating suite input directories"

    set +x
    ref_src_dir="$(find "${ROOT_DATA_DIR}" -type d -path "*/input/${REF_SUITE_ID}" -print -quit)"
    eval_src_dir="$(find "${ROOT_DATA_DIR}" -type d -path "*/input/${SUITE_ID}" -print -quit)"
    set -x

    if [[ -z "${ref_src_dir}" ]]; then
        echo "log.err: Could not find REF suite input directory for ${REF_SUITE_ID} under ${ROOT_DATA_DIR}" >&2
        exit 1
    fi

    if [[ -z "${eval_src_dir}" ]]; then
        echo "log.err: Could not find EVAL suite input directory for ${SUITE_ID} under ${ROOT_DATA_DIR}" >&2
        exit 1
    fi

    echo "[INFO] Copying REF raw data: ${ref_src_dir}"
    cp -a "${ref_src_dir}" "${RAW_DATA_DIR}/"

    echo "[INFO] Copying EVAL raw data: ${eval_src_dir}"
    cp -a "${eval_src_dir}" "${RAW_DATA_DIR}/"

    echo "[INFO] Raw suite input directories copied to ${RAW_DATA_DIR}"
else
    echo "[INFO] RAW_DATA_DIR is not set, skipping raw data copy"
fi
