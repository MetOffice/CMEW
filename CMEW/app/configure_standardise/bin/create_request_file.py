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


def get_arguments():
    """Get arguments from the command line.
    Returns
    -------
    args : argparse.Namespace object
        Refer to the add_argument() calls below, which are self-documenting.
    """
    # Missing arguments will cause the program to exit with error 2.
    parser = argparse.ArgumentParser(
        prog="create_request_file",
        description="Create a request file to pass to CDDS_convert",
    )
    parser.add_argument("--path", help="Path of request-file ", required=True)
    parser.add_argument("--model_id", help="Model_id", required=True)
    parser.add_argument("--suite_id", help="Suite_id", required=True)
    parser.add_argument("--calendar", help="Calendar", required=True)
    parser.add_argument("--variant", help="Variant Label", required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_arguments()
    request = create_request(
        args.model_id, args.suite_id, args.calendar, args.variant
    )
    write_request(request, args.path)
    return request


if __name__ == "__main__":
    main()
