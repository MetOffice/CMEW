# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Unit tests for extract_variable_cubes.py"""
import importlib.util
from pathlib import Path

import iris
import numpy as np
import pytest
from iris.coords import AuxCoord, DimCoord
from iris.cube import Cube, CubeList

iris.FUTURE.save_split_attrs = True


_script_path = (
    Path(__file__).parent.parent.parent
    / "extract_variable_cubes"
    / "bin"
    / "extract_variable_cubes.py"
)

_spec = importlib.util.spec_from_file_location(
    "extract_variable_cubes", _script_path
)
extract_variable_cubes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(extract_variable_cubes)


def _make_dummy_cube(
    var_name: str = "tas",
    standard_name: str | None = "air_temperature",
    long_name: str | None = None,
    with_time: bool = True,
    shape: tuple[int, ...] = (3,),
) -> Cube:
    """Return a minimal in-memory iris Cube."""
    data = np.zeros(shape, dtype=np.float32)
    cube = Cube(
        data,
        var_name=var_name,
        standard_name=standard_name,
        long_name=long_name,
    )
    if with_time:
        time_coord = DimCoord(
            np.arange(shape[0], dtype=np.float64),
            standard_name="time",
            units="days since 2000-01-01",
        )
        cube.add_dim_coord(time_coord, 0)
    return cube


class TestRetrieveVariableList:
    def test_parses_valid_lines(self, tmp_path):
        content = "AERmon/cdnc: cdnc\nAmon/tas: tas\n"
        p = tmp_path / "vars.txt"
        p.write_text(content)
        result = extract_variable_cubes.retrieve_variable_list(p)
        assert result == [("AERmon", "cdnc"), ("Amon", "tas")]

    def test_skips_empty_lines(self, tmp_path):
        content = "\nAmon/tas: tas\n\n"
        p = tmp_path / "vars.txt"
        p.write_text(content)
        result = extract_variable_cubes.retrieve_variable_list(p)
        assert result == [("Amon", "tas")]

    def test_skips_malformed_token(self, tmp_path):
        content = "tas: no_slash_here\nAmon/tas: tas\n"
        p = tmp_path / "vars.txt"
        p.write_text(content)
        result = extract_variable_cubes.retrieve_variable_list(p)
        assert result == [("Amon", "tas")]

    def test_empty_file_returns_empty_list(self, tmp_path):
        p = tmp_path / "vars.txt"
        p.write_text("")
        result = extract_variable_cubes.retrieve_variable_list(p)
        assert result == []


class TestLoadModelRuns:
    def test_loads_yaml(self, tmp_path):
        content = "u-abc:\n  activity: ESMVal\n  institute: MOHC\n"
        p = tmp_path / "model_runs.yml"
        p.write_text(content)
        result = extract_variable_cubes.load_model_runs(p)
        assert result == {"u-abc": {"activity": "ESMVal", "institute": "MOHC"}}


class TestCubeMatchesVariable:
    def test_matches_var_name(self):
        cube = _make_dummy_cube(var_name="tas")
        assert (
            extract_variable_cubes.cube_matches_variable(cube, "tas") is True
        )

    def test_matches_standard_name(self):
        cube = _make_dummy_cube(var_name="x", standard_name="air_temperature")
        assert (
            extract_variable_cubes.cube_matches_variable(
                cube, "air_temperature"
            )
            is True
        )

    def test_matches_long_name(self):
        cube = _make_dummy_cube(
            var_name="x", standard_name=None, long_name="My Variable"
        )
        assert (
            extract_variable_cubes.cube_matches_variable(cube, "My Variable")
            is True
        )

    def test_no_match(self):
        cube = _make_dummy_cube(var_name="tas")
        assert (
            extract_variable_cubes.cube_matches_variable(cube, "pr") is False
        )


class TestCubeHasTimeCoordinate:
    def test_true_when_time_present(self):
        cube = _make_dummy_cube(with_time=True)
        assert extract_variable_cubes.cube_has_time_coordinate(cube) is True

    def test_false_when_no_time(self):
        cube = _make_dummy_cube(with_time=False)
        assert extract_variable_cubes.cube_has_time_coordinate(cube) is False


class TestSanitizeCubeForOutput:
    def test_removes_orog_by_var_name(self):
        cube = _make_dummy_cube(shape=(3, 2, 2), with_time=True)
        lat = DimCoord([0.0, 1.0], standard_name="latitude", units="degrees")
        lon = DimCoord([0.0, 1.0], standard_name="longitude", units="degrees")
        cube.add_dim_coord(lat, 1)
        cube.add_dim_coord(lon, 2)
        orog = AuxCoord(
            np.zeros((2, 2), dtype=np.float32),
            var_name="orog",
        )
        cube.add_aux_coord(orog, (1, 2))
        cleaned = extract_variable_cubes.sanitize_cube_for_output(cube)
        assert not any(c.var_name == "orog" for c in cleaned.aux_coords)

    def test_removes_surface_altitude_by_standard_name(self):
        cube = _make_dummy_cube(shape=(3, 2, 2), with_time=True)
        lat = DimCoord([0.0, 1.0], standard_name="latitude", units="degrees")
        lon = DimCoord([0.0, 1.0], standard_name="longitude", units="degrees")
        cube.add_dim_coord(lat, 1)
        cube.add_dim_coord(lon, 2)
        orog = AuxCoord(
            np.zeros((2, 2), dtype=np.float32),
            standard_name="surface_altitude",
            units="m",
        )
        cube.add_aux_coord(orog, (1, 2))
        cleaned = extract_variable_cubes.sanitize_cube_for_output(cube)
        assert not any(
            c.standard_name == "surface_altitude" for c in cleaned.aux_coords
        )

    def test_removes_surface_altitude_by_long_name(self):
        cube = _make_dummy_cube(shape=(3, 2, 2), with_time=True)
        lat = DimCoord([0.0, 1.0], standard_name="latitude", units="degrees")
        lon = DimCoord([0.0, 1.0], standard_name="longitude", units="degrees")
        cube.add_dim_coord(lat, 1)
        cube.add_dim_coord(lon, 2)
        orog = AuxCoord(
            np.zeros((2, 2), dtype=np.float32),
            long_name="Surface Altitude",
            units="m",
        )
        cube.add_aux_coord(orog, (1, 2))
        cleaned = extract_variable_cubes.sanitize_cube_for_output(cube)
        assert not any(
            c.long_name == "Surface Altitude" for c in cleaned.aux_coords
        )

    def test_leaves_unrelated_aux_coords_intact(self):
        cube = _make_dummy_cube(shape=(3,), with_time=True)
        aux = AuxCoord(
            np.zeros(3, dtype=np.float32),
            var_name="some_other_coord",
        )
        cube.add_aux_coord(aux, 0)
        cleaned = extract_variable_cubes.sanitize_cube_for_output(cube)
        assert any(
            c.var_name == "some_other_coord" for c in cleaned.aux_coords
        )

    def test_returns_copy_not_original(self):
        cube = _make_dummy_cube()
        cleaned = extract_variable_cubes.sanitize_cube_for_output(cube)
        assert cleaned is not cube


class TestPickMatchingCube:
    def test_returns_unique_timed_match(self):
        cube = _make_dummy_cube(var_name="tas", with_time=True)
        result = extract_variable_cubes.pick_matching_cube(
            CubeList([cube]), "tas", Path("dummy.nc")
        )
        assert result is cube

    def test_prefers_timed_cube_over_untimed_match(self):
        timed = _make_dummy_cube(var_name="tas", with_time=True)
        untimed = _make_dummy_cube(var_name="tas", with_time=False)
        result = extract_variable_cubes.pick_matching_cube(
            CubeList([untimed, timed]), "tas", Path("dummy.nc")
        )
        assert result is timed

    def test_raises_when_no_match(self):
        cube = _make_dummy_cube(var_name="pr", with_time=True)
        with pytest.raises(ValueError, match="Could not find"):
            extract_variable_cubes.pick_matching_cube(
                CubeList([cube]), "tas", Path("dummy.nc")
            )

    def test_raises_when_match_has_no_time(self):
        cube = _make_dummy_cube(var_name="tas", with_time=False)
        with pytest.raises(ValueError, match="no time coordinate"):
            extract_variable_cubes.pick_matching_cube(
                CubeList([cube]), "tas", Path("dummy.nc")
            )

    def test_raises_on_multiple_timed_matches_without_var_name(self):
        c1 = _make_dummy_cube(
            var_name="other", standard_name="air_temperature", with_time=True
        )
        c2 = _make_dummy_cube(
            var_name="other2", standard_name="air_temperature", with_time=True
        )
        with pytest.raises(ValueError, match="multiple timed cubes"):
            extract_variable_cubes.pick_matching_cube(
                CubeList([c1, c2]), "air_temperature", Path("dummy.nc")
            )

    def test_uses_var_name_to_disambiguate_multiple_timed_matches(self):
        c1 = _make_dummy_cube(
            var_name="tas", standard_name="air_temperature", with_time=True
        )
        c2 = _make_dummy_cube(
            var_name="other", standard_name="air_temperature", with_time=True
        )
        result = extract_variable_cubes.pick_matching_cube(
            CubeList([c1, c2]), "tas", Path("dummy.nc")
        )
        assert result is c1

    def test_ignores_orog_cube_not_matching_variable(self):
        orog = _make_dummy_cube(
            var_name="orog",
            standard_name="surface_altitude",
            with_time=False,
        )
        tas = _make_dummy_cube(var_name="tas", with_time=True)
        result = extract_variable_cubes.pick_matching_cube(
            CubeList([orog, tas]), "tas", Path("dummy.nc")
        )
        assert result is tas


class TestFindFiles:
    def test_returns_sorted_nc_files(self, tmp_path):
        config = {
            "activity": "ESMVal",
            "institute": "MOHC",
            "model_id": "UKESM1-0-LL",
            "experiment_id": "amip-u-abc",
            "variant_label": "r1i1p1f1",
        }
        base = (
            tmp_path
            / "GCModelDev"
            / "ESMVal"
            / "MOHC"
            / "UKESM1-0-LL"
            / "amip-u-abc"
            / "r1i1p1f1"
            / "Amon"
            / "tas"
        )
        base.mkdir(parents=True)
        (base / "tas_b.nc").touch()
        (base / "tas_a.nc").touch()
        result = extract_variable_cubes.find_files(
            tmp_path, config, "Amon", "tas"
        )
        assert [f.name for f in result] == ["tas_a.nc", "tas_b.nc"]

    def test_returns_empty_when_dir_missing(self, tmp_path):
        config = {
            "activity": "ESMVal",
            "institute": "MOHC",
            "model_id": "UKESM1-0-LL",
            "experiment_id": "amip-u-abc",
            "variant_label": "r1i1p1f1",
        }
        result = extract_variable_cubes.find_files(
            tmp_path, config, "Amon", "missing_var"
        )
        assert result == []


class TestOverwriteWithSingleCube:
    def test_skips_file_when_no_match(self, tmp_path, caplog):
        """overwrite_with_single_cube warns and leaves file untouched."""
        nc_path = tmp_path / "test.nc"
        cube = _make_dummy_cube(var_name="pr", with_time=True)
        iris.save(cube, str(nc_path))

        import logging

        with caplog.at_level(logging.WARNING):
            extract_variable_cubes.overwrite_with_single_cube(nc_path, "tas")

        assert "Skipping" in caplog.text
        # File should still exist and still contain 'pr'
        reloaded = iris.load(str(nc_path))
        assert any(c.var_name == "pr" for c in reloaded)

    def test_overwrites_file_with_correct_cube(self, tmp_path):
        nc_path = tmp_path / "test.nc"
        tas = _make_dummy_cube(var_name="tas", with_time=True)
        pr = _make_dummy_cube(var_name="pr", with_time=False)
        iris.save(CubeList([tas, pr]), str(nc_path))

        extract_variable_cubes.overwrite_with_single_cube(nc_path, "tas")

        reloaded = iris.load(str(nc_path))
        assert len(reloaded) == 1
        assert (
            reloaded[0].var_name == "tas"
        )  # pyright: ignore[reportAttributeAccessIssue]

    def test_temp_file_cleaned_up(self, tmp_path):
        nc_path = tmp_path / "test.nc"
        cube = _make_dummy_cube(var_name="tas", with_time=True)
        iris.save(cube, str(nc_path))

        extract_variable_cubes.overwrite_with_single_cube(nc_path, "tas")

        temp_path = nc_path.with_suffix(".tmp.nc")
        assert not temp_path.exists()
