#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path

import pytest

import run_cdds_with_time_repair


@pytest.fixture(autouse=True)
def parent_workflow_id(monkeypatch):
    """Run wrapper tests as if they are inside a CMEW parent workflow."""
    monkeypatch.setenv("CYLC_WORKFLOW_ID", "CMEW/run13")


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
{simulation_line}

[data]
model_workflow_id = u-eb014
streams = onm

[conversion]
cylc_args = {cylc_args}
"""


def write_request(
    tmp_path,
    cylc_args="--no-detach -v",
    simulation=False,
):
    simulation_line = (
        "simulation = {}".format(simulation) if simulation else ""
    )
    request_path = tmp_path / "request_u-eb014.cfg"
    request_path.write_text(
        REQUEST_CONTENTS.format(
            root_proc_dir=str(tmp_path / "proc"),
            root_data_dir=str(tmp_path / "data"),
            cylc_args=cylc_args,
            simulation_line=simulation_line,
        )
    )
    return str(request_path)


def test_sanitise_workflow_id():
    assert (
        run_cdds_with_time_repair.sanitise_workflow_id("CMEW/run13")
        == "CMEW_run13"
    )


def test_parent_scoped_request_preserves_original(tmp_path):
    request_path = write_request(tmp_path)
    original_contents = Path(request_path).read_text()

    scoped_request_path = (
        run_cdds_with_time_repair.create_parent_scoped_request(
            request_path, "CMEW/run13"
        )
    )

    assert Path(request_path).read_text() == original_contents
    assert scoped_request_path == str(
        tmp_path / "request_u-eb014_CMEW_run13.cfg"
    )

    scoped_config = run_cdds_with_time_repair.read_request(
        scoped_request_path
    )
    assert (
        scoped_config["common"]["workflow_basename"]
        == "u-eb014_CMEW_run13"
    )


def test_parent_scoped_paths_are_unique(tmp_path):
    request_path = write_request(tmp_path)

    scoped_request_path = (
        run_cdds_with_time_repair.create_parent_scoped_request(
            request_path, "CMEW/run13"
        )
    )
    scoped_config = run_cdds_with_time_repair.read_request(
        scoped_request_path
    )

    assert run_cdds_with_time_repair.derive_workflow_dir(
        scoped_config
    ).endswith(
        "/convert/cdds_u-eb014_CMEW_run13"
    )
    # CDDS extraction is keyed by model_workflow_id, so making the nested
    # Cylc workflow name parent-specific must not change the archive data
    # extraction path.
    assert run_cdds_with_time_repair.derive_input_dir(
        scoped_config
    ).endswith(
        "/input/u-eb014/onm"
    )


def test_calls_cdds_convert_patch_then_cylc_vip_in_order(
    monkeypatch, tmp_path
):
    request_path = write_request(tmp_path)
    calls = []

    def fake_run(command, check):
        calls.append(command)
        assert check is True

    def fake_patch(workflow_dir, repair_script, input_dir):
        calls.append(("patch", workflow_dir, repair_script, input_dir))

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", fake_patch
    )

    run_cdds_with_time_repair.main(
        [
            "--request-path",
            request_path,
            "--repair-script",
            "/installed/repair_nemo_time_metadata.py",
        ]
    )

    scoped_request_path = str(
        tmp_path / "request_u-eb014_CMEW_run13.cfg"
    )
    assert calls[0] == [
        "cdds_convert",
        scoped_request_path,
        "--no-submit",
    ]
    assert calls[1][0] == "patch"
    assert calls[2][0] == "cylc"


def test_workflow_name_and_no_run_name_present(monkeypatch, tmp_path):
    request_path = write_request(tmp_path)
    cylc_commands = []

    def fake_run(command, check):
        if command[0] == "cylc":
            cylc_commands.append(command)

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", lambda *a: None
    )

    run_cdds_with_time_repair.main(
        [
            "--request-path",
            request_path,
            "--repair-script",
            "/installed/repair_nemo_time_metadata.py",
        ]
    )

    command = cylc_commands[0]
    assert command[:2] == ["cylc", "vip"]
    assert "--no-run-name" in command
    assert "--workflow-name" in command
    assert command[command.index("--workflow-name") + 1] == (
        "cdds_u-eb014_CMEW_run13"
    )


def test_cylc_args_preserved(monkeypatch, tmp_path):
    request_path = write_request(tmp_path, cylc_args="--no-detach -v")
    cylc_commands = []

    def fake_run(command, check):
        if command[0] == "cylc":
            cylc_commands.append(command)

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", lambda *a: None
    )

    run_cdds_with_time_repair.main(
        [
            "--request-path",
            request_path,
            "--repair-script",
            "/installed/repair_nemo_time_metadata.py",
        ]
    )

    command = cylc_commands[0]
    assert command[-2:] == ["--no-detach", "-v"]


def test_simulation_mode_preserved(monkeypatch, tmp_path):
    request_path = write_request(tmp_path, simulation=True)
    cylc_commands = []

    def fake_run(command, check):
        if command[0] == "cylc":
            cylc_commands.append(command)

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", lambda *a: None
    )

    run_cdds_with_time_repair.main(
        [
            "--request-path",
            request_path,
            "--repair-script",
            "/installed/repair_nemo_time_metadata.py",
        ]
    )

    command = cylc_commands[0]
    assert "--mode=simulation" in command
    assert command.index("--mode=simulation") < command.index("--no-detach")


def test_simulation_mode_absent_when_disabled(monkeypatch, tmp_path):
    request_path = write_request(tmp_path, simulation=False)
    cylc_commands = []

    def fake_run(command, check):
        if command[0] == "cylc":
            cylc_commands.append(command)

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", lambda *a: None
    )

    run_cdds_with_time_repair.main(
        [
            "--request-path",
            request_path,
            "--repair-script",
            "/installed/repair_nemo_time_metadata.py",
        ]
    )

    assert "--mode=simulation" not in cylc_commands[0]


def test_failed_cdds_convert_prevents_patch_and_submit(monkeypatch, tmp_path):
    request_path = write_request(tmp_path)
    calls = []

    def fake_run(command, check):
        if command[0] == "cdds_convert":
            raise run_cdds_with_time_repair.subprocess.CalledProcessError(
                1, command
            )
        calls.append(command)

    def fake_patch(*args):
        calls.append(("patch",) + args)

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", fake_patch
    )

    with pytest.raises(
        run_cdds_with_time_repair.subprocess.CalledProcessError
    ):
        run_cdds_with_time_repair.main(
            [
                "--request-path",
                request_path,
                "--repair-script",
                "/installed/repair_nemo_time_metadata.py",
            ]
        )

    assert calls == []


def test_failed_patch_prevents_submit(monkeypatch, tmp_path):
    request_path = write_request(tmp_path)
    calls = []

    def fake_run(command, check):
        calls.append(command)

    def fake_patch(*args):
        raise ValueError("patch failed")

    monkeypatch.setattr(run_cdds_with_time_repair.subprocess, "run", fake_run)
    monkeypatch.setattr(
        run_cdds_with_time_repair, "patch_run_extract_app", fake_patch
    )

    with pytest.raises(ValueError, match="patch failed"):
        run_cdds_with_time_repair.main(
            [
                "--request-path",
                request_path,
                "--repair-script",
                "/installed/repair_nemo_time_metadata.py",
            ]
        )

    assert calls == [[
        "cdds_convert",
        str(tmp_path / "request_u-eb014_CMEW_run13.cfg"),
        "--no-submit",
    ]]
