#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os

import standardise_ony_annual


def test_model_run_metadata_from_yaml(tmp_path):
    model_runs_yml_fp = tmp_path / "model_runs.yml"
    model_runs_yml_fp.write_text(
        "u-eb014:\n"
        "  model_id: UKESM1-0-LL\n"
        "  experiment_id: test-u-eb014\n"
        "  variant_label: r1i1p1f1\n"
    )

    model_id, experiment_id, variant_label = (
        standardise_ony_annual.model_run_metadata_from_yaml(
            str(model_runs_yml_fp), "u-eb014"
        )
    )

    assert model_id == "UKESM1-0-LL"
    assert experiment_id == "test-u-eb014"
    assert variant_label == "r1i1p1f1"


def test_model_ancillaries_from_json(tmp_path):
    model_ancillaries_fp = tmp_path / "model_ancillaries.json"
    model_ancillaries_fp.write_text(
        '{"UKESM1-0-LL": {'
        '"ancil_files": "/a.pp", '
        '"hybrid_heights_files": "/b.txt", '
        '"replacement_coordinate_files": "/c.nc", '
        '"sites_file": "/d.txt"}}'
    )

    (
        ancil_files,
        hybrid_heights_files,
        replacement_coordinate_files,
        sites_file,
    ) = standardise_ony_annual.model_ancillaries_from_json(
        str(model_ancillaries_fp), "UKESM1-0-LL"
    )

    assert ancil_files == "/a.pp"
    assert hybrid_heights_files == "/b.txt"
    assert replacement_coordinate_files == "/c.nc"
    assert sites_file == "/d.txt"


def test_main_resolves_metadata_from_model_runs_yml(monkeypatch, tmp_path):
    written = {}

    def fake_write_cfg(cfg_path, **template_values):
        written.update(template_values)
        return ""

    monkeypatch.setattr(
        standardise_ony_annual, "retrieve_annual_files", lambda *a, **k: []
    )
    monkeypatch.setattr(
        standardise_ony_annual, "repair_annual_files", lambda *a, **k: None
    )
    monkeypatch.setattr(
        standardise_ony_annual, "write_mip_convert_cfg", fake_write_cfg
    )
    monkeypatch.setattr(
        standardise_ony_annual, "run_standalone_mip_convert", lambda *a: None
    )

    model_runs_yml_fp = tmp_path / "model_runs.yml"
    model_runs_yml_fp.write_text(
        "u-eb014:\n"
        "  model_id: UKESM1-0-LL\n"
        "  experiment_id: test-u-eb014\n"
        "  variant_label: r1i1p1f1\n"
    )

    standardise_ony_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1850",
            "--model-runs-yml-fp",
            str(model_runs_yml_fp),
            "--ancil-files",
            "/tmp/ancil.pp",
            "--hybrid-heights-files",
            "/tmp/hybrid.txt",
            "--replacement-coordinate-files",
            "/tmp/coords.nc",
            "--sites-file",
            "/tmp/sites.txt",
            "--retrieval-dir",
            str(tmp_path / "retrieval"),
            "--model-output-dir",
            str(tmp_path / "input"),
            "--output-dir",
            str(tmp_path / "output"),
            "--cfg-path",
            str(tmp_path / "mip_convert.cfg"),
            "--cmor-log-file",
            str(tmp_path / "cmor.log"),
            "--datestamp",
            "2026-10-11T0000Z",
        ]
    )

    assert written["model_id"] == "UKESM1-0-LL"
    assert written["experiment_id"] == "test-u-eb014"
    assert written["variant_label"] == "r1i1p1f1"


def test_main_requires_metadata_source(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="Must supply"):
        standardise_ony_annual.main(
            [
                "--suite-id",
                "u-eb014",
                "--start-year",
                "1850",
                "--end-year",
                "1850",
                "--ancil-files",
                "/tmp/ancil.pp",
                "--hybrid-heights-files",
                "/tmp/hybrid.txt",
                "--replacement-coordinate-files",
                "/tmp/coords.nc",
                "--sites-file",
                "/tmp/sites.txt",
                "--retrieval-dir",
                str(tmp_path / "retrieval"),
                "--model-output-dir",
                str(tmp_path / "input"),
                "--output-dir",
                str(tmp_path / "output"),
                "--cfg-path",
                str(tmp_path / "mip_convert.cfg"),
                "--cmor-log-file",
                str(tmp_path / "cmor.log"),
                "--datestamp",
                "2026-10-11T0000Z",
            ]
        )


def test_ensure_directories_creates_missing_directories(tmp_path):
    retrieval_dir = tmp_path / "retrieval"
    output_dir = tmp_path / "output"
    cfg_path = tmp_path / "cfg" / "mip_convert.cfg"
    cmor_log_file = tmp_path / "log" / "cmor.log"

    standardise_ony_annual.ensure_directories(
        str(retrieval_dir), str(output_dir), str(cfg_path), str(cmor_log_file)
    )

    assert retrieval_dir.is_dir()
    assert output_dir.is_dir()
    assert cfg_path.parent.is_dir()
    assert cmor_log_file.parent.is_dir()


def test_ensure_directories_is_idempotent_for_existing_directories(tmp_path):
    retrieval_dir = tmp_path / "retrieval"
    output_dir = tmp_path / "output"
    cfg_path = tmp_path / "cfg" / "mip_convert.cfg"
    cmor_log_file = tmp_path / "log" / "cmor.log"

    # Simulate a Cylc retry/restart: the directories already exist from
    # a previous attempt.
    standardise_ony_annual.ensure_directories(
        str(retrieval_dir), str(output_dir), str(cfg_path), str(cmor_log_file)
    )
    standardise_ony_annual.ensure_directories(
        str(retrieval_dir), str(output_dir), str(cfg_path), str(cmor_log_file)
    )

    assert retrieval_dir.is_dir()
    assert output_dir.is_dir()


def test_main_creates_directories_before_running_mip_convert(
    monkeypatch, tmp_path
):
    calls = []

    retrieval_dir = tmp_path / "retrieval"
    output_dir = tmp_path / "output"
    cfg_path = tmp_path / "cfg" / "mip_convert.cfg"
    cmor_log_file = tmp_path / "log" / "cmor.log"

    monkeypatch.setattr(
        standardise_ony_annual, "retrieve_annual_files", lambda *a, **k: []
    )
    monkeypatch.setattr(
        standardise_ony_annual, "repair_annual_files", lambda *a, **k: None
    )
    monkeypatch.setattr(
        standardise_ony_annual, "write_mip_convert_cfg", lambda *a, **k: ""
    )

    def fake_run_mip_convert(*args):
        # Required directories must already exist by the time
        # mip_convert is invoked.
        calls.append(args)
        assert retrieval_dir.is_dir()
        assert output_dir.is_dir()
        assert cfg_path.parent.is_dir()
        assert cmor_log_file.parent.is_dir()

    monkeypatch.setattr(
        standardise_ony_annual,
        "run_standalone_mip_convert",
        fake_run_mip_convert,
    )

    standardise_ony_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1850",
            "--model-id",
            "UKESM1-0-LL",
            "--experiment-id",
            "test-u-eb014",
            "--variant-label",
            "r1i1p1f1",
            "--ancil-files",
            "/tmp/ancil.pp",
            "--hybrid-heights-files",
            "/tmp/hybrid.txt",
            "--replacement-coordinate-files",
            "/tmp/coords.nc",
            "--sites-file",
            "/tmp/sites.txt",
            "--retrieval-dir",
            str(retrieval_dir),
            "--model-output-dir",
            str(tmp_path / "input"),
            "--output-dir",
            str(output_dir),
            "--cfg-path",
            str(cfg_path),
            "--cmor-log-file",
            str(cmor_log_file),
            "--datestamp",
            "2026-10-11T0000Z",
        ]
    )

    assert len(calls) == 1


def test_main_resolves_ancillaries_from_model_ancillaries_fp(
    monkeypatch, tmp_path
):
    written = {}

    def fake_write_cfg(cfg_path, **template_values):
        written.update(template_values)
        return ""

    monkeypatch.setattr(
        standardise_ony_annual, "retrieve_annual_files", lambda *a, **k: []
    )
    monkeypatch.setattr(
        standardise_ony_annual, "repair_annual_files", lambda *a, **k: None
    )
    monkeypatch.setattr(
        standardise_ony_annual, "write_mip_convert_cfg", fake_write_cfg
    )
    monkeypatch.setattr(
        standardise_ony_annual, "run_standalone_mip_convert", lambda *a: None
    )

    model_ancillaries_fp = tmp_path / "model_ancillaries.json"
    model_ancillaries_fp.write_text(
        '{"UKESM1-0-LL": {'
        '"ancil_files": "/a.pp", '
        '"hybrid_heights_files": "/b.txt", '
        '"replacement_coordinate_files": "/c.nc", '
        '"sites_file": "/d.txt"}}'
    )

    standardise_ony_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1850",
            "--model-id",
            "UKESM1-0-LL",
            "--experiment-id",
            "test-u-eb014",
            "--variant-label",
            "r1i1p1f1",
            "--model-ancillaries-fp",
            str(model_ancillaries_fp),
            "--retrieval-dir",
            str(tmp_path / "retrieval"),
            "--model-output-dir",
            str(tmp_path / "input"),
            "--output-dir",
            str(tmp_path / "output"),
            "--cfg-path",
            str(tmp_path / "mip_convert.cfg"),
            "--cmor-log-file",
            str(tmp_path / "cmor.log"),
            "--datestamp",
            "2026-10-11T0000Z",
        ]
    )

    assert written["ancil_files"] == "/a.pp"
    assert written["hybrid_heights_files"] == "/b.txt"
    assert written["replacement_coordinate_files"] == "/c.nc"
    assert written["sites_file"] == "/d.txt"


def test_main_requires_ancillary_source(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="Must supply --ancil-files"):
        standardise_ony_annual.main(
            [
                "--suite-id",
                "u-eb014",
                "--start-year",
                "1850",
                "--end-year",
                "1850",
                "--model-id",
                "UKESM1-0-LL",
                "--experiment-id",
                "test-u-eb014",
                "--variant-label",
                "r1i1p1f1",
                "--retrieval-dir",
                str(tmp_path / "retrieval"),
                "--model-output-dir",
                str(tmp_path / "input"),
                "--output-dir",
                str(tmp_path / "output"),
                "--cfg-path",
                str(tmp_path / "mip_convert.cfg"),
                "--cmor-log-file",
                str(tmp_path / "cmor.log"),
                "--datestamp",
                "2026-10-11T0000Z",
            ]
        )


def test_retrieve_annual_files_calls_moo_get_per_year(monkeypatch, tmp_path):
    calls = []

    def fake_run(command, check):
        calls.append(command)
        assert check is True

    monkeypatch.setattr(standardise_ony_annual.subprocess, "run", fake_run)

    retrieved = standardise_ony_annual.retrieve_annual_files(
        "u-eb014", 1850, 1851, str(tmp_path)
    )

    assert len(calls) == 2
    assert calls[0][:2] == ["moo", "get"]
    assert (
        "moose:/crum/u-eb014/ony.nc.file/"
        "nemo_eb014o_1y_18501201-18511201_grid-T.nc" in calls[0]
    )
    assert (
        "moose:/crum/u-eb014/ony.nc.file/"
        "nemo_eb014o_1y_18511201-18521201_grid-T.nc" in calls[1]
    )
    assert len(retrieved) == 2
    assert retrieved[0].endswith("nemo_eb014o_1y_18501201-18511201_grid-T.nc")


def test_retrieve_annual_files_skips_moo_get_when_file_already_exists(
    monkeypatch, tmp_path
):
    calls = []

    def fake_run(command, check):
        calls.append(command)

    monkeypatch.setattr(standardise_ony_annual.subprocess, "run", fake_run)

    existing_path = os.path.join(
        str(tmp_path), "nemo_eb014o_1y_18501201-18511201_grid-T.nc"
    )
    with open(existing_path, "w") as file_handle:
        file_handle.write("")

    retrieved = standardise_ony_annual.retrieve_annual_files(
        "u-eb014", 1850, 1850, str(tmp_path)
    )

    assert calls == []
    assert retrieved == [existing_path]


def test_retrieve_annual_files_calls_moo_get_when_file_missing(
    monkeypatch, tmp_path
):
    calls = []

    def fake_run(command, check):
        calls.append(command)

    monkeypatch.setattr(standardise_ony_annual.subprocess, "run", fake_run)

    retrieved = standardise_ony_annual.retrieve_annual_files(
        "u-eb014", 1850, 1850, str(tmp_path)
    )

    assert len(calls) == 1
    assert calls[0][:2] == ["moo", "get"]
    assert retrieved == [
        os.path.join(
            str(tmp_path), "nemo_eb014o_1y_18501201-18511201_grid-T.nc"
        )
    ]


def test_retrieve_annual_files_returns_same_paths_existing_or_missing(
    monkeypatch, tmp_path
):
    def fake_run(command, check):
        pass

    monkeypatch.setattr(standardise_ony_annual.subprocess, "run", fake_run)

    missing_case = standardise_ony_annual.retrieve_annual_files(
        "u-eb014", 1850, 1850, str(tmp_path / "missing")
    )

    existing_dir = tmp_path / "existing"
    existing_dir.mkdir()
    (existing_dir / "nemo_eb014o_1y_18501201-18511201_grid-T.nc").write_text(
        ""
    )
    existing_case = standardise_ony_annual.retrieve_annual_files(
        "u-eb014", 1850, 1850, str(existing_dir)
    )

    assert [os.path.basename(p) for p in missing_case] == [
        os.path.basename(p) for p in existing_case
    ]


def test_write_mip_convert_cfg_contains_annual_plugin_and_table(tmp_path):
    cfg_path = str(tmp_path / "mip_convert.cfg")

    contents = standardise_ony_annual.write_mip_convert_cfg(
        cfg_path,
        cmor_log_file="/tmp/cmor.log",
        mip_table_dir="/tmp/tables",
        calendar="gregorian",
        experiment_id="test-u-eb014",
        grid="Native eORCA1",
        grid_label="gn",
        institution_id="MOHC",
        license="test-license",
        model_id="UKESM1-0-LL",
        output_dir="/tmp/output",
        variant_label="r1i1p1f1",
        ancil_files="/tmp/ancil.pp",
        atmos_timestep="1200",
        hybrid_heights_files="/tmp/hybrid.txt",
        plugin_location="/tmp/plugin",
        model_output_dir="/tmp/input",
        replacement_coordinate_files="/tmp/coords.nc",
        run_bounds_start="1851-01-01T00:00:00",
        run_bounds_end="1852-01-01T00:00:00",
        sites_file="/tmp/sites.txt",
        suite_id="u-eb014",
        variables=" ".join(standardise_ony_annual.ANNUAL_VARIABLES),
    )

    assert os.path.isfile(cfg_path)
    assert "mip_convert_external_plugin = cmew_mip_convert_plugin" in contents
    assert "mip_convert_external_plugin_location = /tmp/plugin" in contents
    assert "mip_convert_plugin = CMEWGCModelDevAnnual" in contents
    assert "mip_table_dir = /tmp/tables" in contents
    assert "run_bounds = 1851-01-01T00:00:00 1852-01-01T00:00:00" in contents
    assert "[stream_ony_grid-T]" in contents
    assert "GCModelDev_Oyr = tos sos thetao so" in contents


def test_run_standalone_mip_convert_does_not_use_cdds_entry_points(
    monkeypatch, tmp_path
):
    calls = []

    def fake_run(command, check):
        calls.append(command)

    monkeypatch.setattr(standardise_ony_annual.subprocess, "run", fake_run)

    standardise_ony_annual.run_standalone_mip_convert(
        str(tmp_path / "mip_convert.cfg"), "2026-10-11T0000Z"
    )

    assert len(calls) == 1
    command = calls[0]
    assert command[0] == "mip_convert"
    assert "cdds_convert" not in command
    assert "cdds_extract" not in command
    assert "run_mip_convert" not in command
    assert "-s" in command and command[command.index("-s") + 1] == "ony"


def test_main_computes_calendar_year_run_bounds(monkeypatch, tmp_path):
    written = {}

    def fake_write_cfg(cfg_path, **template_values):
        written.update(template_values)
        return ""

    monkeypatch.setattr(
        standardise_ony_annual, "retrieve_annual_files", lambda *a, **k: []
    )
    monkeypatch.setattr(
        standardise_ony_annual, "repair_annual_files", lambda *a, **k: None
    )
    monkeypatch.setattr(
        standardise_ony_annual, "write_mip_convert_cfg", fake_write_cfg
    )
    monkeypatch.setattr(
        standardise_ony_annual, "run_standalone_mip_convert", lambda *a: None
    )

    standardise_ony_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1850",
            "--model-id",
            "UKESM1-0-LL",
            "--experiment-id",
            "test-u-eb014",
            "--variant-label",
            "r1i1p1f1",
            "--ancil-files",
            "/tmp/ancil.pp",
            "--hybrid-heights-files",
            "/tmp/hybrid.txt",
            "--replacement-coordinate-files",
            "/tmp/coords.nc",
            "--sites-file",
            "/tmp/sites.txt",
            "--retrieval-dir",
            str(tmp_path / "retrieval"),
            "--model-output-dir",
            str(tmp_path / "input"),
            "--output-dir",
            str(tmp_path / "output"),
            "--cfg-path",
            str(tmp_path / "mip_convert.cfg"),
            "--cmor-log-file",
            str(tmp_path / "cmor.log"),
            "--datestamp",
            "2026-10-11T0000Z",
        ]
    )

    # Archive file spans 1850-12-01 to 1851-12-01, so the calendar year
    # containing its midpoint is 1851.
    assert written["run_bounds_start"] == "1851-01-01T00:00:00"
    assert written["run_bounds_end"] == "1852-01-01T00:00:00"


def test_annual_variables_from_recipe(tmp_path):
    recipe_variables_file = tmp_path / "recipe_variables.txt"
    recipe_variables_file.write_text(
        "Omon/tos\n" "Omon/sos\n" "Omon/thetao\n" "Omon/so\n"
    )

    actual = standardise_ony_annual.annual_variables_from_recipe(
        str(recipe_variables_file)
    )

    assert actual == ["tos", "sos", "thetao", "so"]


def test_annual_variables_from_recipe_removes_duplicates(tmp_path):
    recipe_variables_file = tmp_path / "recipe_variables.txt"
    recipe_variables_file.write_text("Omon/tos\n" "Omon/tos\n" "Omon/sos\n")

    actual = standardise_ony_annual.annual_variables_from_recipe(
        str(recipe_variables_file)
    )

    assert actual == ["tos", "sos"]


def test_annual_variables_from_recipe_rejects_unsupported_variable(tmp_path):
    import pytest

    recipe_variables_file = tmp_path / "recipe_variables.txt"
    recipe_variables_file.write_text("Omon/tos\n" "Amon/tas\n")

    with pytest.raises(
        ValueError,
        match="does not support recipe variables: tas",
    ):
        standardise_ony_annual.annual_variables_from_recipe(
            str(recipe_variables_file)
        )


def test_annual_variables_from_recipe_rejects_malformed_entry(tmp_path):
    import pytest

    recipe_variables_file = tmp_path / "recipe_variables.txt"
    recipe_variables_file.write_text("tos\n")

    with pytest.raises(
        ValueError,
        match="expected '<mip>/<short_name>'",
    ):
        standardise_ony_annual.annual_variables_from_recipe(
            str(recipe_variables_file)
        )


def test_main_uses_recipe_variables_file(monkeypatch, tmp_path):
    """Main should request only annual variables required by the recipe."""
    written = {}

    def fake_write_cfg(cfg_path, **template_values):
        written.update(template_values)
        return ""

    monkeypatch.setattr(
        standardise_ony_annual,
        "retrieve_annual_files",
        lambda *a, **k: [],
    )
    monkeypatch.setattr(
        standardise_ony_annual,
        "repair_annual_files",
        lambda *a, **k: None,
    )
    monkeypatch.setattr(
        standardise_ony_annual,
        "write_mip_convert_cfg",
        fake_write_cfg,
    )
    monkeypatch.setattr(
        standardise_ony_annual,
        "run_standalone_mip_convert",
        lambda *a: None,
    )

    recipe_variables_file = tmp_path / "ocean_variables.txt"
    recipe_variables_file.write_text("Omon/tos\n")

    standardise_ony_annual.main(
        [
            "--suite-id",
            "u-eb014",
            "--start-year",
            "1850",
            "--end-year",
            "1850",
            "--model-id",
            "UKESM1-0-LL",
            "--experiment-id",
            "test-u-eb014",
            "--variant-label",
            "r1i1p1f1",
            "--ancil-files",
            "/tmp/ancil.pp",
            "--hybrid-heights-files",
            "/tmp/hybrid.txt",
            "--replacement-coordinate-files",
            "/tmp/coords.nc",
            "--sites-file",
            "/tmp/sites.txt",
            "--recipe-variables-file",
            str(recipe_variables_file),
            "--retrieval-dir",
            str(tmp_path / "retrieval"),
            "--model-output-dir",
            str(tmp_path / "input"),
            "--output-dir",
            str(tmp_path / "output"),
            "--cfg-path",
            str(tmp_path / "mip_convert.cfg"),
            "--cmor-log-file",
            str(tmp_path / "cmor.log"),
            "--datestamp",
            "2026-10-12T0000Z",
        ]
    )

    assert written["variables"] == "tos"
