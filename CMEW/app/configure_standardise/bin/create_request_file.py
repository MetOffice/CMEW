#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request.json file from the ESMValTool recipe.
"""
import os
import argparse
import json


def create_request(model_id, suite_id, calendar, variant_label):
    """Retrieve CDDS request information from Rose suite configuration.
    Parameters
    ----------
    model_id: string of the model_id
    suite_id: string of the suite_id
    calendar: string of the calendar
    variant_label: string of the variant label

    Returns
    -------
    dict
        CDDS request information to be written to JSON file.
    """

    streams = ["apm"]
    start_datetime = f"{os.environ['START_YEAR']}-01-01T00:00:00"
    end_year = int(os.environ["START_YEAR"]) + int(
        os.environ["NUMBER_OF_YEARS"]
    )
    end_datetime = f"{end_year}-01-01T00:00:00"
    run_bounds = f"{start_datetime} {end_datetime}"
    streams_run_bounds = {
        f"run_bounds_for_stream_{stream}": run_bounds for stream in streams
    }
    request = {
        "atmos_timestep": "1200",
        "branch_method": "no parent",
        "calendar": calendar,
        "child_base_date": "1850-01-01T00:00:00",
        "config_version": "1.0.1",
        "experiment_id": "amip",
        "external_plugin": "",
        "external_plugin_location": "",
        "global_attributes": {},
        "institution_id": os.environ["INSTITUTION_ID"],
        "license": "GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mass_data_class": "crum",
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "mip_table_dir": "/home/h03/cdds/etc/mip_tables/GCModelDev/0.0.9",
        "model_id": model_id,
        "model_type": "AGCM AER",
        "package": "round-1",
        "request_id": "CMEW",
        "run_bounds": run_bounds,
        "sub_experiment_id": "none",
        "suite_branch": "trunk",
        "suite_id": suite_id,
        "suite_revision": "not used except with data request",
        "variant_label": variant_label,
    }
    # Combine request dict and streams_run_bounds dict (in-place union).
    request |= streams_run_bounds
    return request


def write_request(request, target_path):
    """Write request dictionary to a JSON file at ``target_path``.

    Parameters
    ----------
    request : dict
        Dictionary containing the request information.

    target_path: Path
        Location to write the request file.
    """
    with open(target_path, mode="w") as file:
        json.dump(request, file, separators=(",\n", ": "))


def make_request_file(
    request_file_path, model_id, suite_id, calendar, variant
):
    """Drive creation of a request file at``request_file_path``.
       This also facilitates unit testing by providing a target for an
       injected file path.
    Parameters
    ----------
    request_file_path: A file path string.
        The location to which to write the request file.
    model_id: string of the model_id
    suite_id: string of the suite_id
    calendar: string of the calendar
    variant: string of the variant label
    """
    request = create_request(model_id, suite_id, calendar, variant)
    write_request(request, request_file_path)
    return request


def main():
    # Get args from cmd line.  This needs to be told which of test or reference
    # settings to use, it cannot decide itself.
    # Mandatory flags or missing arguments for a flag are handled by the parser
    # Optional flags must be handled explicitly unless given a default value.
    parser = argparse.ArgumentParser(
        prog="create-request-file",
        description="Create a request file to pass to CDDS-convert",
    )
    parser.add_argument("-p", help="Request-file path", required=True)
    parser.add_argument("-m", help="Model_id", required=True)
    parser.add_argument("-s", help="Suite_id", required=True)
    parser.add_argument("-c", help="Calendar", required=True)
    parser.add_argument("-v", help="Variant Label", required=True)
    args = parser.parse_args()

    make_request_file(args.p, args.m, args.s, args.c, args.v)


if __name__ == "__main__":
    main()
