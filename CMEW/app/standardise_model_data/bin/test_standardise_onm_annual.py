#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

from pathlib import Path

import pytest

import standardise_onm_annual


def test_annual_variables_from_recipe_accepts_supported_variables(tmp_path):
    variables_file = tmp_path / "variables.txt"
    variables_file.write_text(
        "Oyr/tos\n"
        "Oyr/sos\n"
        "Oyr/thetao\n"
        "Oyr/so\n"
    )

    assert standardise_onm_annual.annual_variables_from_recipe(
        variables_file
    ) == ["tos", "sos", "thetao", "so"]


def test_retrieve_monthly_files_builds_calendar_month_names(
    tmp_path, monkeypatch
):
    calls = []

    def fake_run(command, check):
        calls.append(command)

    monkeypatch.setattr(
        standardise_onm_annual.subprocess,
        "run",
        fake_run,
    )

    retrieved = standardise_onm_annual.retrieve_monthly_files(
        "u-eb014",
        1850,
        1850,
        str(tmp_path),
    )

    assert len(retrieved) == 12
    assert Path(retrieved[0]).name == (
        "nemo_eb014o_1m_18500101-18500201_grid-T.nc"
    )
    assert Path(retrieved[-1]).name == (
        "nemo_eb014o_1m_18501201-18510101_grid-T.nc"
    )
    assert len(calls) == 12


def test_run_standalone_mip_convert_uses_onm_stream(monkeypatch):
    commands = []

    def fake_run(command, check):
        commands.append(command)

    monkeypatch.setattr(
        standardise_onm_annual.subprocess,
        "run",
        fake_run,
    )

    standardise_onm_annual.run_standalone_mip_convert(
        "/tmp/test.cfg",
        "2026-10-15T1200Z",
    )

    command = commands[0]
    assert "-s" in command
    assert command[command.index("-s") + 1] == "onm"


def test_main_processes_each_year_and_cleans_after_success(
    tmp_path, monkeypatch
):
    events = []
    staged_by_year = {}

    def fake_retrieve(suite_id, start_year, end_year, destination_dir):
        assert start_year == end_year
        year = start_year
        paths = []
        for month in range(1, 13):
            path = tmp_path / f"{year}-{month:02d}.nc"
            path.write_text("staged")
            paths.append(str(path))
        staged_by_year[year] = paths
        events.append(("retrieve", year))
        return paths

    def fake_repair(path):
        year = int(Path(path).name.split("-", 1)[0])
        events.append(("repair", year))

    cfg_bounds = []

    def fake_write_cfg(cfg_path, **values):
        cfg_bounds.append(
            (
                values["run_bounds_start"],
                values["run_bounds_end"],
            )
        )
        events.append(
            ("cfg", int(values["run_bounds_start"][:4]))
        )

    def fake_convert(cfg_path, datestamp):
        year = int(cfg_bounds[-1][0][:4])
        events.append(("convert", year))

    monkeypatch.setattr(
        standardise_onm_annual,
        "retrieve_monthly_files",
        fake_retrieve,
    )
    monkeypatch.setattr(
        standardise_onm_annual.repair_nemo_time_metadata,
        "repair_file",
        fake_repair,
    )
    monkeypatch.setattr(
        standardise_onm_annual,
        "write_mip_convert_cfg",
        fake_write_cfg,
    )
    monkeypatch.setattr(
        standardise_onm_annual,
        "run_standalone_mip_convert",
        fake_convert,
    )

    model_runs = tmp_path / "model_runs.yml"
    model_runs.write_text(
        "u-eb014:\n"
        "  model_id: UKESM1-0-LL\n"
        "  experiment_id: test-u-eb014\n"
        "  variant_label: r1i1p1f1\n"
    )

    ancillaries = tmp_path / "ancillaries.json"
    ancillaries.write_text(
        """{
  "UKESM1-0-LL": {
    "ancil_files": "ancil",
    "hybrid_heights_files": "hybrid",
    "replacement_coordinate_files": "coords",
    "sites_file": "sites"
  }
}
"""
    )

    variables = tmp_path / "variables.txt"
    variables.write_text("Oyr/tos\n")

    standardise_onm_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1851",
            "--model-runs-yml-fp",
            str(model_runs),
            "--model-ancillaries-fp",
            str(ancillaries),
            "--recipe-variables-file",
            str(variables),
            "--retrieval-dir",
            str(tmp_path / "retrieval"),
            "--model-output-dir",
            str(tmp_path / "model-output"),
            "--output-dir",
            str(tmp_path / "output"),
            "--cfg-path",
            str(tmp_path / "annual.cfg"),
            "--cmor-log-file",
            str(tmp_path / "cmor.log"),
            "--datestamp",
            "2026-10-15T1200Z",
        ]
    )

    assert cfg_bounds == [
        ("1850-01-01T00:00:00", "1851-01-01T00:00:00"),
        ("1851-01-01T00:00:00", "1852-01-01T00:00:00"),
    ]

    for year in (1850, 1851):
        assert ("retrieve", year) in events
        assert ("convert", year) in events
        for path in staged_by_year[year]:
            assert not Path(path).exists()


def test_main_keeps_staged_files_if_conversion_fails(
    tmp_path, monkeypatch
):
    staged = []

    def fake_retrieve(*args):
        for month in range(1, 13):
            path = tmp_path / f"1850-{month:02d}.nc"
            path.write_text("staged")
            staged.append(path)
        return [str(path) for path in staged]

    monkeypatch.setattr(
        standardise_onm_annual,
        "retrieve_monthly_files",
        fake_retrieve,
    )
    monkeypatch.setattr(
        standardise_onm_annual.repair_nemo_time_metadata,
        "repair_file",
        lambda path: None,
    )
    monkeypatch.setattr(
        standardise_onm_annual,
        "write_mip_convert_cfg",
        lambda *args, **kwargs: None,
    )

    def fail_convert(*args):
        raise RuntimeError("conversion failed")

    monkeypatch.setattr(
        standardise_onm_annual,
        "run_standalone_mip_convert",
        fail_convert,
    )

    model_runs = tmp_path / "model_runs.yml"
    model_runs.write_text(
        "u-eb014:\n"
        "  model_id: UKESM1-0-LL\n"
        "  experiment_id: test-u-eb014\n"
        "  variant_label: r1i1p1f1\n"
    )

    ancillaries = tmp_path / "ancillaries.json"
    ancillaries.write_text(
        """{
  "UKESM1-0-LL": {
    "ancil_files": "ancil",
    "hybrid_heights_files": "hybrid",
    "replacement_coordinate_files": "coords",
    "sites_file": "sites"
  }
}
"""
    )

    variables = tmp_path / "variables.txt"
    variables.write_text("Oyr/tos\n")

    with pytest.raises(RuntimeError, match="conversion failed"):
        standardise_onm_annual.main(
            [
                "--suite-id",
                "u-eb014",
                "--start-year",
                "1850",
                "--end-year",
                "1850",
                "--model-runs-yml-fp",
                str(model_runs),
                "--model-ancillaries-fp",
                str(ancillaries),
                "--recipe-variables-file",
                str(variables),
                "--retrieval-dir",
                str(tmp_path / "retrieval"),
                "--model-output-dir",
                str(tmp_path / "model-output"),
                "--output-dir",
                str(tmp_path / "output"),
                "--cfg-path",
                str(tmp_path / "annual.cfg"),
                "--cmor-log-file",
                str(tmp_path / "cmor.log"),
                "--datestamp",
                "2026-10-15T1200Z",
            ]
        )

    assert all(path.exists() for path in staged)
