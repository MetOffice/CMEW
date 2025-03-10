# (C) Crown Copyright 2024-2025, Met Office.
# The LICENSE.md file contains full licensing details.
import pytest
from create_request_file import make_request_file

# Testing app/configure_standardise/bin/create_request_file.py
# To see the request file produced, run pytest from CMEW with the arguments:
# CMEW/app/configure_standardise/bin/test_create_request_file.py -s

test_file = "request.cfg"  # Result file to be checked


@pytest.fixture
def monkey_env(monkeypatch):
    monkeypatch.setenv("START_YEAR", "1993")
    monkeypatch.setenv("NUMBER_OF_YEARS", "1")
    monkeypatch.setenv("MODEL_ID", "UKESM1-0-LL")
    monkeypatch.setenv("CALENDAR", "360_day")
    monkeypatch.setenv("INSTITUTION_ID", "MOHC")
    monkeypatch.setenv("SUITE_ID", "u-az513")
    monkeypatch.setenv("ROOT_PROC_DIR", "~/cylc-run/CMEW/runX/share/proc")
    monkeypatch.setenv("ROOT_DATA_DIR", "~/cylc-run/CMEW/runX/share/data")
    monkeypatch.setenv(
        "VARIABLES_PATH", "~/cylc-run/CMEW/runX/share/etc/variables.txt"
    )


@pytest.fixture
def request_file_path(tmp_path):
    # path to new result file
    filepath = tmp_path / test_file
    return filepath


def test_make_request_file(monkey_env, request_file_path):  # noqa : 36
    # Create a CDDS request file and compare it to the expected result file.
    # noqa : 36 : Ignore warning about monkey_env not being used; it is needed
    # but not referenced.
    print(f"Request file: {request_file_path}")  # run with -s option for this
    actual = make_request_file(request_file_path)
    assert actual is not None, "Request was not produced"
    assert actual == expected_request(), "Request produced did not match"


def expected_request():
    expect = [
        "[metadata]",
        "branch_date_in_child =",
        "branch_date_in_parent =",
        "branch_method = no parent",
        "base_date = 1850-01-01T00:00:00Z",
        "calendar = 360_day",
        "experiment_id = amip",
        "institution_id = MOHC",
        "license = GCModelDev model data is licensed under the Open Government License v3 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)",  # noqa: E501
        "mip = ESMVal",
        "mip_era = GCModelDev",
        # "parent_base_date =",
        # "parent_experiment_id = no parent",
        # "parent_mip =",
        # "parent_mip_era =",
        # "parent_model_id =",
        # "parent_time_units =",
        # "parent_variant_label =",
        "sub_experiment_id = none",
        "variant_label = r1i1p1f1",
        "model_id = UKESM1-0-LL",
        "model_type = AGCM AER",
        "",
        "[netcdf_global_attributes]",
        "parent_experiment_id = no parent",
        "",
        "[common]",
        "force_plugin =",
        "external_plugin =",
        "external_plugin_location =",
        "mip_table_dir = $CDDS_ETC/mip_tables/GCModelDev/0.0.23",
        "mode = relaxed",
        "package = round-1",
        "workflow_basename = CMEW",
        "root_proc_dir = ~/cylc-run/CMEW/runX/share/proc",
        "root_data_dir = ~/cylc-run/CMEW/runX/share/data",
        "root_ancil_dir = $CDDS_ETC/ancil",
        "root_hybrid_heights_dir = $CDDS_ETC/vertical_coordinates",
        "root_replacement_coordinates_dir = $CDDS_ETC/horizontal_coordinates",
        "sites_file = $CDDS_ETC/cfmip2/cfmip2-sites-orog.txt",
        "standard_names_version = latest",
        "standard_names_dir = $CDDS_ETC/standard_names",
        "simulation = False",
        "log_level = INFO",
        "",
        "[data]",
        "data_version =",
        "end_date = 1994-01-01T00:00:00Z",
        "mass_data_class = crum",
        "mass_ensemble_member =",
        "start_date = 1993-01-01T00:00:00Z",
        "model_workflow_id = u-az513",
        "model_workflow_branch = trunk",
        "model_workflow_revision = not used except with data request",
        "streams = apm",
        "variable_list_file = ~/cylc-run/CMEW/runX/share/etc/variables.txt",
        "output_mass_root =",
        "output_mass_suffix =",
        "max_file_size = 20000000000.0",
        "",
        "[misc]",
        "atmos_timestep = 1200",
        "use_proc_dir = True",
        "no_overwrite = False",
        "halo_removal_latitude =",
        "halo_removal_longitude =",
        "force_coordinate_rotation = False",
        "",
        "[inventory]",
        "inventory_check = False",
        "inventory_database_location =",
        "",
        "[conversion]",
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
    return expect
