#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
from datetime import datetime

import netCDF4
import pytest

from repair_nemo_time_metadata import (
    TIME_CALENDAR,
    TIME_ORIGIN,
    TIME_UNITS,
    parse_dates_from_filename,
    repair_file,
)


def make_nemo_file(path, time_counter_value=0, missing_variable=None):
    """Create a minimal NEMO-like grid-T NetCDF file with broken time."""
    with netCDF4.Dataset(path, "w") as dataset:
        dataset.createDimension("time_counter", None)
        dataset.createDimension("axis_nbounds", 2)

        variables = {
            "time_counter": ("time_counter",),
            "time_centered": ("time_counter",),
            "time_counter_bounds": ("time_counter", "axis_nbounds"),
            "time_centered_bounds": ("time_counter", "axis_nbounds"),
        }
        for name, dims in variables.items():
            if name == missing_variable:
                continue
            variable = dataset.createVariable(name, "f8", dims)
            variable.units = "seconds since 1950-01-01 00:00:00"
            variable.calendar = "gregorian"
            # Explicit indexing creates exactly one record on the
            # unlimited time_counter dimension, matching a broken file
            # before repair.
            if dims == ("time_counter",):
                variable[0] = time_counter_value
            else:
                variable[0, :] = [time_counter_value, time_counter_value]


def test_repair_normal_january_file(tmp_path):
    filepath = tmp_path / "nemo_eb014o_1m_18500101-18500201_grid-T.nc"
    make_nemo_file(filepath)

    repair_file(str(filepath))

    start_date = datetime(1850, 1, 1)
    end_date = datetime(1850, 2, 1)
    mid_date = start_date + (end_date - start_date) / 2
    expected_start = (start_date - TIME_ORIGIN).total_seconds()
    expected_mid = (mid_date - TIME_ORIGIN).total_seconds()
    expected_end = (end_date - TIME_ORIGIN).total_seconds()

    with netCDF4.Dataset(filepath, "r") as dataset:
        assert len(dataset.dimensions["time_counter"]) == 1
        for name in ("time_counter", "time_centered"):
            variable = dataset.variables[name]
            assert variable[:].item() == expected_mid
            assert variable.units == TIME_UNITS
            assert variable.calendar == TIME_CALENDAR
        for name in ("time_counter_bounds", "time_centered_bounds"):
            variable = dataset.variables[name]
            assert list(variable[:].flatten()) == [
                expected_start,
                expected_end,
            ]
            assert variable.units == TIME_UNITS
            assert variable.calendar == TIME_CALENDAR


def test_repair_cross_year_file(tmp_path):
    filepath = tmp_path / "nemo_eb014o_1m_18501201-18510101_grid-T.nc"
    make_nemo_file(filepath)

    repair_file(str(filepath))

    start_date = datetime(1850, 12, 1)
    end_date = datetime(1851, 1, 1)
    mid_date = start_date + (end_date - start_date) / 2
    expected_mid = (mid_date - TIME_ORIGIN).total_seconds()

    with netCDF4.Dataset(filepath, "r") as dataset:
        assert len(dataset.dimensions["time_counter"]) == 1
        assert dataset.variables["time_counter"][:].item() == expected_mid


def test_malformed_filename_raises(tmp_path):
    filepath = tmp_path / "nemo_eb014o_1m_grid-T.nc"
    make_nemo_file(filepath)

    with pytest.raises(
        ValueError, match="does not match the expected pattern"
    ):
        repair_file(str(filepath))


def test_missing_time_variable_raises(tmp_path):
    filepath = tmp_path / "nemo_eb014o_1m_18500101-18500201_grid-T.nc"
    make_nemo_file(filepath, missing_variable="time_centered")

    with pytest.raises(ValueError, match="time_centered.*not found"):
        repair_file(str(filepath))


def test_end_date_not_later_than_start_raises(tmp_path):
    filepath = tmp_path / "nemo_eb014o_1m_18500201-18500101_grid-T.nc"
    make_nemo_file(filepath)

    with pytest.raises(ValueError, match="is not later than start date"):
        repair_file(str(filepath))


def test_parse_dates_from_filename():
    start_date, end_date = parse_dates_from_filename(
        "/some/dir/nemo_eb014o_1m_18500101-18500201_grid-T.nc"
    )
    assert start_date == datetime(1850, 1, 1)
    assert end_date == datetime(1850, 2, 1)
