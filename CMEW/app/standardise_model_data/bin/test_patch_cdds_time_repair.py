#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
import shlex

import pytest

from patch_cdds_time_repair import (
    ORIGINAL_COMMAND,
    build_repair_command,
    derive_input_dir,
    derive_workflow_dir,
    patch_run_extract_app,
    read_request,
)

REQUEST_CONTENTS = """\
[metadata]
mip_era = GCModelDev
mip = ESMVal
model_id = UKESM1-0-LL
experiment_id = test-u-eb014
variant_label = r1i1p1f1

[common]
root_proc_dir = {root_proc_dir}
root_data_dir = {root_data_dir}
package = round-1
workflow_basename = u-eb014

[data]
model_workflow_id = u-eb014
streams = {streams}
"""


def write_request(tmp_path, root_proc_dir, root_data_dir, streams="onm"):
    request_path = tmp_path / "request_u-eb014.cfg"
    request_path.write_text(
        REQUEST_CONTENTS.format(
            root_proc_dir=root_proc_dir,
            root_data_dir=root_data_dir,
            streams=streams,
        )
    )
    return str(request_path)


def make_run_extract_app(workflow_dir, command=ORIGINAL_COMMAND):
    run_extract_dir = os.path.join(workflow_dir, "app", "run_extract")
    os.makedirs(run_extract_dir, exist_ok=True)
    rose_app_path = os.path.join(run_extract_dir, "rose-app.conf")
    with open(rose_app_path, "w") as file_handle:
        file_handle.write(
            "[command]\n"
            "default={}\n"
            "\n"
            "[env]\n"
            "setup=${{SETUP_CMD}}\n".format(command)
        )
    return rose_app_path


def test_derive_workflow_dir(tmp_path):
    request_path = write_request(tmp_path, "/proc", "/data")
    config = read_request(request_path)

    workflow_dir = derive_workflow_dir(config)

    assert workflow_dir == (
        "/proc/GCModelDev/ESMVal/"
        "UKESM1-0-LL_test-u-eb014_r1i1p1f1/round-1/convert/cdds_u-eb014"
    )


def test_derive_input_dir(tmp_path):
    request_path = write_request(tmp_path, "/proc", "/data")
    config = read_request(request_path)

    input_dir = derive_input_dir(config)

    assert input_dir == (
        "/data/GCModelDev/ESMVal/"
        "UKESM1-0-LL_test-u-eb014_r1i1p1f1/round-1/input/u-eb014/onm"
    )


def test_patch_injects_repair_command(tmp_path):
    request_path = write_request(
        tmp_path, str(tmp_path / "proc"), str(tmp_path / "data")
    )
    config = read_request(request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)
    rose_app_path = make_run_extract_app(workflow_dir)

    patch_run_extract_app(
        workflow_dir, "/path/to/repair_nemo_time_metadata.py", input_dir
    )

    contents = open(rose_app_path).read()
    assert ORIGINAL_COMMAND in contents
    assert "&&" in contents
    assert "repair_nemo_time_metadata.py" in contents
    assert input_dir in contents


def test_patch_is_idempotent(tmp_path):
    request_path = write_request(
        tmp_path, str(tmp_path / "proc"), str(tmp_path / "data")
    )
    config = read_request(request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)
    rose_app_path = make_run_extract_app(workflow_dir)

    patch_run_extract_app(
        workflow_dir, "/path/to/repair_nemo_time_metadata.py", input_dir
    )
    first_contents = open(rose_app_path).read()

    patch_run_extract_app(
        workflow_dir, "/path/to/repair_nemo_time_metadata.py", input_dir
    )
    second_contents = open(rose_app_path).read()

    assert first_contents == second_contents
    assert second_contents.count("repair_nemo_time_metadata.py") == 1


def test_missing_generated_rose_app_raises(tmp_path):
    request_path = write_request(
        tmp_path, str(tmp_path / "proc"), str(tmp_path / "data")
    )
    config = read_request(request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)
    os.makedirs(workflow_dir, exist_ok=True)

    with pytest.raises(
        FileNotFoundError, match="run_extract Rose app not found"
    ):
        patch_run_extract_app(
            workflow_dir, "/path/to/repair_nemo_time_metadata.py", input_dir
        )


def test_missing_workflow_dir_raises(tmp_path):
    request_path = write_request(
        tmp_path, str(tmp_path / "proc"), str(tmp_path / "data")
    )
    config = read_request(request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)

    with pytest.raises(
        FileNotFoundError, match="workflow directory not found"
    ):
        patch_run_extract_app(
            workflow_dir, "/path/to/repair_nemo_time_metadata.py", input_dir
        )


def test_unsupported_stream_raises(tmp_path):
    request_path = write_request(
        tmp_path,
        str(tmp_path / "proc"),
        str(tmp_path / "data"),
        streams="apm inm",
    )
    config = read_request(request_path)

    with pytest.raises(ValueError, match="Unsupported streams"):
        derive_input_dir(config)


def test_build_repair_command_quotes_input_dir_with_spaces():
    input_dir = "/data/round 1/input/u-eb014/onm"

    command = build_repair_command(
        "/installed/repair_nemo_time_metadata.py", input_dir
    )

    assert command.endswith(
        "{}/nemo_*_1m_*_grid-T.nc".format(shlex.quote(input_dir))
    )
    assert "'/nemo_*_1m_*_grid-T.nc'" not in command
