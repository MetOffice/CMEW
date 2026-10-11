#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Repair broken internal time metadata in extracted NEMO monthly
grid-T files, using the correct dates encoded in the filename.
"""
import argparse
import os
import re
import sys
import logging
from datetime import datetime, timedelta

import netCDF4

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)

# These NEMO files contain unreliable internal time coordinates, while
# the extraction filenames retain the correct archive period. Rebuild
# the time axis from the filename before CDDS/MIP Convert validates it.
FILENAME_DATE_PATTERN = re.compile(r"_(\d{8})-(\d{8})_grid-T\.nc$")

TIME_UNITS = "seconds since 1850-01-01 00:00:00"
TIME_CALENDAR = "gregorian"
TIME_ORIGIN = datetime(1850, 1, 1, 0, 0, 0)

TIME_VARIABLES = (
    "time_counter",
    "time_centered",
    "time_counter_bounds",
    "time_centered_bounds",
)


def parse_dates_from_filename(filepath):
    """
    Parse the start and end dates encoded in a NEMO extraction filename.

    Parameters
    ----------
    filepath : str
        The full path to the NEMO NetCDF file.

    Returns
    -------
    tuple[datetime, datetime]
        The start and end dates of the file's archive period.
    """
    match = FILENAME_DATE_PATTERN.search(os.path.basename(filepath))
    if not match:
        raise ValueError(
            "Filename does not match the expected pattern "
            "'_YYYYMMDD-YYYYMMDD_grid-T.nc': {}".format(filepath)
        )

    start_date = datetime.strptime(match.group(1), "%Y%m%d")
    end_date = datetime.strptime(match.group(2), "%Y%m%d")

    if end_date <= start_date:
        raise ValueError(
            "End date {} is not later than start date {} in: {}".format(
                end_date, start_date, filepath
            )
        )

    return start_date, end_date


def repair_file(filepath):
    """
    Repair the time metadata of a single NEMO grid-T file in place.

    Parameters
    ----------
    filepath : str
        The full path to the NEMO NetCDF file to repair.
    """
    logger.info("Repairing file %s", filepath)

    start_date, end_date = parse_dates_from_filename(filepath)
    mid_date = start_date + (end_date - start_date) / 2

    print("Repairing {}".format(filepath))
    print("  start: {}".format(start_date))
    print("  mid:   {}".format(mid_date))
    print("  end:   {}".format(end_date))

    start_seconds = (start_date - TIME_ORIGIN).total_seconds()
    mid_seconds = (mid_date - TIME_ORIGIN).total_seconds()
    end_seconds = (end_date - TIME_ORIGIN).total_seconds()

    with netCDF4.Dataset(filepath, "r+") as dataset:
        for var_name in TIME_VARIABLES:
            if var_name not in dataset.variables:
                raise ValueError(
                    "Required time variable '{}' not found in: {}".format(
                        var_name, filepath
                    )
                )

        for var_name in ("time_counter", "time_centered"):
            variable = dataset.variables[var_name]
            # time_counter is an unlimited dimension, so an explicit index
            # must be used here rather than `[:]`, which would otherwise
            # extend the dimension instead of writing to the single record.
            variable[0] = mid_seconds
            variable.units = TIME_UNITS
            variable.calendar = TIME_CALENDAR

        for var_name in ("time_counter_bounds", "time_centered_bounds"):
            variable = dataset.variables[var_name]
            # Likewise, index the unlimited time_counter dimension
            # explicitly to avoid extending it to two records.
            variable[0, :] = [start_seconds, end_seconds]
            variable.units = TIME_UNITS
            variable.calendar = TIME_CALENDAR


def parse_args(arguments):
    """
    Return the names and values of the command line arguments for
    the repair script.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.

    Returns
    -------
    :class:`argparse.Namespace`
        The names and values of the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Repair broken time metadata in extracted NEMO grid-T files, "
            "using the dates encoded in each filename."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "filepaths",
        nargs="+",
        help="One or more extracted NEMO grid-T NetCDF files to repair.",
    )
    return parser.parse_args(arguments)


def main(arguments=None):
    """
    Repair the time metadata of the supplied NEMO grid-T files.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    args = parse_args(arguments)
    for filepath in args.filepaths:
        repair_file(filepath)


if __name__ == "__main__":
    main()
