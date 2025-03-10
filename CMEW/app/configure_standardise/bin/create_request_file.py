#!/usr/bin/env python
# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Generates the request.cfg file from the ESMValTool recipe for CDDS v3.
Guidance can be found in `CDDS config_request`_.

.. _CDDS config_request: https://fuzzy-adventure-c51c3985.pages.github.io/latest/tutorials/request/config_request/  # noqa: E501
"""
import os
from pathlib import Path
from typing import List


def create_request() -> List[str]:
    """Retrieve CDDS request information from Rose suite configuration.

    Returns
    -------
        List[Str]
        CDDS request information to be written to a CDDS .cfg file.
    """
    # Tried this with a configparser.ConfigParser, which was a cleaner
    # implementation, instead of a List[str] but it could not control
    # whitespace sufficiently.

    # date/time given in ISO 8601 format, where the Z terminating character
    # represents timezone UTC (equivalent of GMT).
    start_year = os.environ["START_YEAR"]
    number_of_years = os.environ["NUMBER_OF_YEARS"]
    model_id = os.environ["MODEL_ID"]
    calendar = os.environ["CALENDAR"]
    institution_id = os.environ["INSTITUTION_ID"]
    suite_id = os.environ["SUITE_ID"]
    root_proc_dir = os.environ["ROOT_PROC_DIR"]
    root_data_dir = os.environ["ROOT_DATA_DIR"]
    variables_path = os.environ["VARIABLES_PATH"]

    start_datetime = f"{start_year}-01-01T00:00:00Z"
    end_year = int(start_year) + int(number_of_years)
    end_datetime = f"{end_year}-01-01T00:00:00Z"
    base_date = "1850-01-01T00:00:00Z"
    # time_units = "days since " + base_date[0:10]  # date part yyyy-mm-dd
    mip_table_v = "0.0.23"
    mip_table_dir = "$CDDS_ETC" + "/mip_tables/GCModelDev/" + mip_table_v

    section_spacer = ""
    request = [
        "[metadata]",  # **** SECTION
        "branch_date_in_child =",
        "branch_date_in_parent =",
        "branch_method = no parent",
        f"base_date = {base_date}",
        f"calendar = {calendar}",
        "experiment_id = amip",
        f"institution_id = {institution_id}",
        "license = GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip = ESMVal",
        "mip_era = GCModelDev",
        # f"parent_base_date = {base_date}",
        # "parent_base_date =",
        # "parent_experiment_id = no parent",
        # "parent_mip =",
        # "parent_mip_era =",
        # f"parent_model_id = {model_id}",
        # "parent_model_id =",
        # f"parent_time_units = {time_units}",
        # "parent_time_units =",
        # "parent_variant_label =",
        "sub_experiment_id = none",
        "variant_label = r1i1p1f1",
        f"model_id = {model_id}",
        "model_type = AGCM AER",
        section_spacer,
        #
        "[netcdf_global_attributes]",  # **** SECTION
        "parent_experiment_id = no parent",
        section_spacer,
        #
        "[common]",  # **** SECTION
        "force_plugin =",
        "external_plugin =",
        "external_plugin_location =",
        f"mip_table_dir = {mip_table_dir}",
        "mode = relaxed",
        "package = round-1",
        "workflow_basename = CMEW",
        f"root_proc_dir = {root_proc_dir}",
        f"root_data_dir = {root_data_dir}",
        "root_ancil_dir = $CDDS_ETC" + "/ancil",
        "root_hybrid_heights_dir = $CDDS_ETC" + "/vertical_coordinates",
        "root_replacement_coordinates_dir = $CDDS_ETC"
        + "/horizontal_coordinates",
        "sites_file = $CDDS_ETC" + "/cfmip2/cfmip2-sites-orog.txt",
        "standard_names_version = latest",
        "standard_names_dir = $CDDS_ETC" + "/standard_names",
        "simulation = False",
        "log_level = INFO",
        section_spacer,
        #
        "[data]",  # **** SECTION
        "data_version =",
        f"end_date = {end_datetime}",
        "mass_data_class = crum",
        "mass_ensemble_member =",
        f"start_date = {start_datetime}",
        f"model_workflow_id = {suite_id}",
        "model_workflow_branch = trunk",  # svn reference, not git
        "model_workflow_revision = not used except with data request",
        "streams = apm",
        f"variable_list_file = {variables_path}",
        "output_mass_root =",
        "output_mass_suffix =",
        "max_file_size = 20000000000.0",
        section_spacer,
        #
        "[misc]",  # **** SECTION
        "atmos_timestep = 1200",
        "use_proc_dir = True",
        "no_overwrite = False",
        "halo_removal_latitude =",
        "halo_removal_longitude =",
        "force_coordinate_rotation = False",
        section_spacer,
        #
        "[inventory]",  # **** SECTION
        "inventory_check = False",
        "inventory_database_location =",
        section_spacer,
        #
        "[conversion]",  # **** SECTION
        "skip_extract = False",
        "skip_extract_validation = False",
        "skip_configure = False",
        "skip_qc = False",
        "skip_archive = True",
        "cdds_workflow_branch = tags/3.0.6",
        "cylc_args = -v --no-detach",
        "no_email_notifications = True",
        "scale_memory_limits =",
        "override_cycling_frequency =",
        "slicing =",
        "model_params_dir =",
        "continue_if_mip_convert_failed = False",
        "delete_preexisting_proc_dir = False",
        "delete_preexisting_data_dir = False",
    ]
    return request


def write_request(request: List[str], target_path: Path):
    """Write request to a .cfg file at ``target_path``.

    Parameters
    ----------
    request : List of Strings
        A List containing the request information.

    target_path: Path
        Location to write the request file.
    """
    with open(target_path, mode="w", encoding="utf-8") as fw:
        fw.write("\n".join(request))


def make_request_file(request_file_path):
    """Drive creation of a request file at``request_file_path``.
       This also facilitates unit testing by providing a target for an
       injected file path.
    Parameters
    ----------
    request_file_path: A file path string.
        The location to which to write the request file.
    """
    request = create_request()
    write_request(request, request_file_path)
    return request


def main():
    target_path = (
        Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "etc" / "request.cfg"
    )
    make_request_file(target_path)


if __name__ == "__main__":
    main()
