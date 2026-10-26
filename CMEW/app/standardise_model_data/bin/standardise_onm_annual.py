#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Standardise monthly NEMO ``onm`` grid-T data to annual ``Oyr`` using
standalone mip_convert.

This is a separate, opt-in path alongside the existing monthly ``onm``
route (via ``cdds_convert``/``cdds_extract``/``run_mip_convert``). It is
used only for datasets configured to source ocean variables from the
monthly ``onm`` archive stream and annualises it to calendar-year
``Oyr`` output.

The sequence is:
    MASS retrieval (moo get) of the requested annual period
        -> write a standalone mip_convert.cfg
        -> standalone mip_convert, using the CMEW annual mapping plugin
           and workflow-local GCModelDev_Oyr table.

This never invokes cdds_extract, cdds_convert, or run_mip_convert.
"""
import argparse
import json
import os
import subprocess
import sys
import logging
from pathlib import Path

import yaml

import repair_nemo_time_metadata


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)

# The annual ocean variables supported by the CMEW annual mapping plugin
# and the workflow-local GCModelDev_Oyr table.
ANNUAL_VARIABLES = ["tos", "sos", "thetao", "so"]

ORCA1_GRID = (
    "Native eORCA1 tripolar primarily 1 deg with meridional "
    "refinement down to 1/3 degree in the tropics; "
    "360 x 330 longitude/latitude"
)

NATIVE_VARIABLE_SETS = {
    "orca1": ("tos", "sos", "thetao", "so"),
    "orca025": ("tos_con", "sos_abs", "thetao_con", "so_abs"),
}

NATIVE_GRID_CONFIG = {
    "orca1": {
        "grid": ORCA1_GRID,
        "nominal_resolution": "100 km",
        "halo_removal": "1:-1,1:-1",
        "replacement_coordinate_files": None,
    },
    "orca025": {
        "grid": (
            "Native eORCA025 tripolar primarily 0.25 deg; "
            "1440 x 1205 longitude/latitude"
        ),
        "nominal_resolution": "25 km",
        "halo_removal": "1:,:",
        # TODO: Move this site-specific coordinate file into workflow
        # configuration once ORCA025 ancillary selection is generalised.
        "replacement_coordinate_files": (
            "/home/users/cdds/etc/horizontal_coordinates/"
            "cice_eORCA025_coords.nc"
        ),
    },
}


def detect_native_variable_convention(file_path):
    """Detect the supported native NEMO variable naming convention.

    The established ORCA1 data use ``tos``, ``sos``, ``thetao`` and ``so``.
    The eORCA025 data tested by CMEW use conservative-temperature and
    absolute-salinity names: ``tos_con``, ``sos_abs``, ``thetao_con`` and
    ``so_abs``.
    """
    result = subprocess.run(
        ["ncdump", "-h", file_path],
        check=True,
        capture_output=True,
        text=True,
    )
    header = result.stdout

    for convention, variable_names in NATIVE_VARIABLE_SETS.items():
        if all(" {}(".format(name) in header for name in variable_names):
            logger.info(
                "Detected native NEMO variable convention %s in %s",
                convention,
                file_path,
            )
            return convention

    raise ValueError(
        "Could not identify a supported native NEMO variable convention "
        "in {!r}; expected either {} or {}.".format(
            file_path,
            ", ".join(NATIVE_VARIABLE_SETS["orca1"]),
            ", ".join(NATIVE_VARIABLE_SETS["orca025"]),
        )
    )


def annual_variables_from_recipe(recipe_variables_file):
    """Return supported annual variable names required by a recipe.

    The recipe variables file contains one entry per line in the form
    ``<mip>/<short_name>``. The annual onm route uses the short name and
    writes it using the workflow-local GCModelDev_Oyr table.

    Parameters
    ----------
    recipe_variables_file : str
        Path to the variables file produced by configure_for.

    Returns
    -------
    list[str]
        Unique variable short names, preserving recipe order.

    Raises
    ------
    ValueError
        If an entry is malformed, no variables are found, or the recipe
        requests variables unsupported by the annual onm route.
    """
    variables = []

    with open(recipe_variables_file, "r") as file_handle:
        for line in file_handle:
            entry = line.strip()
            if not entry:
                continue

            if "/" not in entry:
                raise ValueError(
                    "Invalid recipe variable entry {!r}; expected "
                    "'<mip>/<short_name>'.".format(entry)
                )

            _, variable = entry.split("/", 1)
            if not variable:
                raise ValueError(
                    "Invalid recipe variable entry {!r}; missing "
                    "short name.".format(entry)
                )

            if variable not in variables:
                variables.append(variable)

    if not variables:
        raise ValueError(
            "No variables found in recipe variables file {}.".format(
                recipe_variables_file
            )
        )

    unsupported = [
        variable for variable in variables if variable not in ANNUAL_VARIABLES
    ]
    if unsupported:
        raise ValueError(
            "Annual onm standardisation does not support recipe "
            "variables: {}. Supported variables: {}.".format(
                ", ".join(unsupported),
                ", ".join(ANNUAL_VARIABLES),
            )
        )

    return variables


MIP_CONVERT_CFG_TEMPLATE = """\
# Generated by standardise_onm_annual.py for the monthly-to-annual
# standardisation route. This is separate from the normal Omon route.

[cmor_setup]
cmor_log_file = {cmor_log_file}
create_subdirectories = 0
mip_table_dir = {mip_table_dir}
netcdf_file_action = CMOR_REPLACE_4

[cmor_dataset]
branch_method = no parent
calendar = {calendar}
experiment_id = {experiment_id}
grid = {grid}
grid_label = {grid_label}
institution_id = {institution_id}
license = {license}
mip = ESMVal
mip_era = GCModelDev
model_id = {model_id}
model_type = AGCM AER
nominal_resolution = {nominal_resolution}
output_dir = {output_dir}
sub_experiment_id = none
variant_label = {variant_label}

[request]
ancil_files = {ancil_files}
ancil_variables =
atmos_timestep = {atmos_timestep}
base_date = 1850-01-01T00:00:00
deflate_level = 2
force_coordinate_rotation = False
hybrid_heights_files = {hybrid_heights_files}
mip_convert_external_plugin = cmew_onm_annual_plugin
mip_convert_external_plugin_location = {plugin_location}
mip_convert_plugin = CMEWGCModelDevOnmAnnual
model_output_dir = {model_output_dir}
replacement_coordinate_files = {replacement_coordinate_files}
run_bounds = {run_bounds_start} {run_bounds_end}
shuffle = True
sites_file = {sites_file}
suite_id = {suite_id}

[global_attributes]
further_info_url = dummy_url

[halo_removal]
stream_onm = {halo_removal}

[stream_onm_grid-T]
GCModelDev_Oyr = {variables}
"""


def retrieve_monthly_files(suite_id, start_year, end_year, destination_dir):
    """
    Retrieve complete calendar years of monthly NEMO ``onm`` grid-T data.

    For each requested year, retrieve the 12 monthly files spanning
    1 January of that year through 1 January of the following year.

    Parameters
    ----------
    suite_id : str
        The model run suite id, e.g. "u-eb014".
    start_year : int
        The first calendar year to retrieve.
    end_year : int
        The last calendar year to retrieve.
    destination_dir : str
        Directory to retrieve the monthly files into.

    Returns
    -------
    list of str
        Full paths to the retrieved monthly files.
    """
    os.makedirs(destination_dir, exist_ok=True)
    retrieved = []

    suite_name = suite_id[-5:]

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            next_year = year
            next_month = month + 1
            if next_month == 13:
                next_month = 1
                next_year += 1

            pattern = ("nemo_{}o_1m_{}{:02d}01-{}{:02d}01_grid-T.nc").format(
                suite_name,
                year,
                month,
                next_year,
                next_month,
            )

            destination_path = os.path.join(destination_dir, pattern)

            if os.path.isfile(destination_path):
                logger.info(
                    "Reusing already-retrieved file %s",
                    destination_path,
                )
            else:
                source = "moose:/crum/{}/onm.nc.file/{}".format(
                    suite_id,
                    pattern,
                )
                logger.info("Retrieving %s", source)
                subprocess.run(
                    ["moo", "get", source, destination_dir + "/"],
                    check=True,
                )

            retrieved.append(destination_path)

    return retrieved


def model_run_metadata_from_yaml(model_runs_yml_fp, suite_id):
    """
    Return the model_id, experiment_id and variant_label for a suite id,
    read from the same model_runs.yml file the monthly onm route already
    uses (generated by copy_datasets). Avoids hard-coding per-dataset
    metadata in the Cylc task definition.

    Parameters
    ----------
    model_runs_yml_fp : str
        The full path to the model_runs.yml file.
    suite_id : str
        The model run suite id, e.g. "u-eb014".

    Returns
    -------
    tuple of str
        (model_id, experiment_id, variant_label)
    """
    with open(model_runs_yml_fp, "r") as file_handle:
        model_runs = yaml.safe_load(file_handle)
    run = model_runs[suite_id]
    return run["model_id"], run["experiment_id"], run["variant_label"]


def model_ancillaries_from_json(model_ancillaries_fp, model_id):
    """
    Return the ancillary/coordinate file paths for a model_id, read from
    a workflow-local JSON file. Centralises these model-specific paths
    so they are owned by model configuration, not hard-coded per-task
    in flow.cylc; a new annual model opts in by adding an entry here.

    Parameters
    ----------
    model_ancillaries_fp : str
        The full path to the model ancillaries JSON file.
    model_id : str
        The model id, e.g. "UKESM1-0-LL".

    Returns
    -------
    tuple of str
        (ancil_files, hybrid_heights_files, replacement_coordinate_files,
        sites_file)
    """
    with open(model_ancillaries_fp, "r") as file_handle:
        model_ancillaries = json.load(file_handle)
    ancillaries = model_ancillaries[model_id]
    return (
        ancillaries["ancil_files"],
        ancillaries["hybrid_heights_files"],
        ancillaries["replacement_coordinate_files"],
        ancillaries["sites_file"],
    )


def write_mip_convert_cfg(cfg_path, **template_values):
    """
    Write the standalone mip_convert cfg file for the annual route.

    Parameters
    ----------
    cfg_path : str
        The full path to write the cfg file to.
    template_values : dict
        The values to substitute into ``MIP_CONVERT_CFG_TEMPLATE``.
    """
    contents = MIP_CONVERT_CFG_TEMPLATE.format(**template_values)
    parent_dir = os.path.dirname(cfg_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    with open(cfg_path, "w") as file_handle:
        file_handle.write(contents)
    return contents


def run_standalone_mip_convert(cfg_path, datestamp, native_convention):
    """
    Run standalone mip_convert against the generated cfg file.

    Does not invoke cdds_extract, cdds_convert, or run_mip_convert.

    Parameters
    ----------
    cfg_path : str
        The full path to the mip_convert cfg file.
    datestamp : str
        The datestamp to pass to mip_convert's ``--datestamp`` option.
    """
    logger.info(
        "Running standalone mip_convert for the annual onm route "
        "using native convention %s",
        native_convention,
    )
    environment = os.environ.copy()
    environment["CMEW_ONM_NATIVE_CONVENTION"] = native_convention

    subprocess.run(
        [
            "mip_convert",
            cfg_path,
            "-a",
            "-s",
            "onm",
            "-l",
            "mip_convert_onm_annual",
            "--datestamp",
            datestamp,
            "--plugin_id",
            "GCModelDev",
            "--relaxed_cmor",
        ],
        check=True,
        env=environment,
    )


def parse_args(arguments):
    """
    Return the names and values of the command line arguments for the
    annual onm standardisation script.

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
            "Standardise monthly NEMO onm grid-T data to annual Oyr "
            "using standalone mip_convert, as an opt-in alternative "
            "to the monthly onm "
            "route."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--suite-id", required=True)
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--end-year", type=int, required=True)
    parser.add_argument(
        "--model-id",
        help=(
            "Required unless --model-runs-yml-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--experiment-id",
        help=(
            "Required unless --model-runs-yml-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--variant-label",
        help=(
            "Required unless --model-runs-yml-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--model-runs-yml-fp",
        help=(
            "The full path to the model_runs.yml file (the same file "
            "the monthly onm route uses) to read model-id/experiment-id/"
            "variant-label from for --suite-id, instead of supplying "
            "them explicitly."
        ),
    )
    parser.add_argument("--institution-id", default="MOHC")
    parser.add_argument(
        "--grid",
        default=ORCA1_GRID,
    )
    parser.add_argument("--grid-label", default="gn")
    parser.add_argument(
        "--license",
        default=(
            "GCModelDev model data is licensed under the "
            "Open Government License v3 "
            "(https://www.nationalarchives.gov.uk/"
            "doc/open-government-licence/version/3/)"
        ),
    )
    parser.add_argument("--atmos-timestep", default="1200")
    parser.add_argument(
        "--ancil-files",
        help=(
            "Required unless --model-ancillaries-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--hybrid-heights-files",
        help=(
            "Required unless --model-ancillaries-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--replacement-coordinate-files",
        help=(
            "Required unless --model-ancillaries-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--sites-file",
        help=(
            "Required unless --model-ancillaries-fp is given, in which "
            "case it is read from there."
        ),
    )
    parser.add_argument(
        "--model-ancillaries-fp",
        help=(
            "The full path to the model ancillaries JSON file to read "
            "--ancil-files/--hybrid-heights-files/"
            "--replacement-coordinate-files/--sites-file from for "
            "--model-id, instead of supplying them explicitly."
        ),
    )
    parser.add_argument("--retrieval-dir", required=True)
    parser.add_argument("--model-output-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--mip-table-dir",
        default=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "mip_tables",
            "GCModelDev",
        ),
    )
    parser.add_argument(
        "--plugin-location",
        default=os.path.dirname(os.path.abspath(__file__)),
    )
    parser.add_argument(
        "--recipe-variables-file",
        help=(
            "Variables file produced by configure_for. When supplied, "
            "the annual route processes only supported variables required "
            "by the selected recipe."
        ),
    )
    parser.add_argument("--cfg-path", required=True)
    parser.add_argument("--cmor-log-file", required=True)
    parser.add_argument("--datestamp", required=True)
    return parser.parse_args(arguments)


def ensure_directories(retrieval_dir, output_dir, cfg_path, cmor_log_file):
    """
    Create all directories this script owns before retrieval/conversion.

    Cylc may retry or restart this task, and mip_convert itself does not
    create its own output directory, so these must be created up front
    and idempotently (safe to call repeatedly, e.g. on a retry, without
    failing if they already exist).

    Parameters
    ----------
    retrieval_dir : str
        The full path to the directory retrieved monthly files are
        written to.
    output_dir : str
        The full path to the directory mip_convert writes output to.
    cfg_path : str
        The full path to the mip_convert cfg file to be written.
    cmor_log_file : str
        The full path to the CMOR log file to be written.
    """
    Path(retrieval_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(cfg_path).parent.mkdir(parents=True, exist_ok=True)
    Path(cmor_log_file).parent.mkdir(parents=True, exist_ok=True)


def main(arguments=None):
    """
    Standardise monthly NEMO onm grid-T data to annual Oyr for one model run.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    args = parse_args(arguments)

    model_id = args.model_id
    experiment_id = args.experiment_id
    variant_label = args.variant_label
    if args.model_runs_yml_fp:
        model_id, experiment_id, variant_label = model_run_metadata_from_yaml(
            args.model_runs_yml_fp, args.suite_id
        )
    if not (model_id and experiment_id and variant_label):
        raise ValueError(
            "Must supply --model-id/--experiment-id/--variant-label, "
            "or --model-runs-yml-fp."
        )

    ancil_files = args.ancil_files
    hybrid_heights_files = args.hybrid_heights_files
    replacement_coordinate_files = args.replacement_coordinate_files
    sites_file = args.sites_file
    if args.model_ancillaries_fp:
        (
            ancil_files,
            hybrid_heights_files,
            replacement_coordinate_files,
            sites_file,
        ) = model_ancillaries_from_json(args.model_ancillaries_fp, model_id)
    if not (
        ancil_files
        and hybrid_heights_files
        and replacement_coordinate_files
        and sites_file
    ):
        raise ValueError(
            "Must supply --ancil-files/--hybrid-heights-files/"
            "--replacement-coordinate-files/--sites-file, or "
            "--model-ancillaries-fp."
        )

    annual_variables = ANNUAL_VARIABLES
    if args.recipe_variables_file:
        annual_variables = annual_variables_from_recipe(
            args.recipe_variables_file
        )

    ensure_directories(
        args.retrieval_dir, args.output_dir, args.cfg_path, args.cmor_log_file
    )

    for year in range(args.start_year, args.end_year + 1):
        logger.info("Processing calendar year %s", year)

        retrieved_files = retrieve_monthly_files(
            args.suite_id,
            year,
            year,
            args.retrieval_dir,
        )

        native_convention = detect_native_variable_convention(
            retrieved_files[0]
        )
        grid_config = NATIVE_GRID_CONFIG[native_convention]

        grid = args.grid
        if native_convention != "orca1" and grid == ORCA1_GRID:
            grid = grid_config["grid"]

        year_replacement_coordinate_files = replacement_coordinate_files
        convention_coordinate_files = grid_config[
            "replacement_coordinate_files"
        ]
        if convention_coordinate_files:
            year_replacement_coordinate_files = convention_coordinate_files

        if not os.path.isfile(year_replacement_coordinate_files):
            raise ValueError(
                "Replacement coordinate file does not exist: {!r}".format(
                    year_replacement_coordinate_files
                )
            )

        logger.info(
            "Using %s grid metadata: grid=%r, nominal_resolution=%s, "
            "halo_removal=%s, replacement_coordinate_files=%s",
            native_convention,
            grid,
            grid_config["nominal_resolution"],
            grid_config["halo_removal"],
            year_replacement_coordinate_files,
        )

        for file_path in retrieved_files:
            logger.info("Repairing monthly time metadata in %s", file_path)
            repair_nemo_time_metadata.repair_file(file_path)

        run_bounds_start = "{}-01-01T00:00:00".format(year)
        run_bounds_end = "{}-01-01T00:00:00".format(year + 1)

        write_mip_convert_cfg(
            args.cfg_path,
            cmor_log_file=args.cmor_log_file,
            mip_table_dir=args.mip_table_dir,
            calendar="gregorian",
            experiment_id=experiment_id,
            grid=grid,
            grid_label=args.grid_label,
            institution_id=args.institution_id,
            license=args.license,
            model_id=model_id,
            nominal_resolution=grid_config["nominal_resolution"],
            output_dir=args.output_dir,
            variant_label=variant_label,
            ancil_files=ancil_files,
            atmos_timestep=args.atmos_timestep,
            hybrid_heights_files=hybrid_heights_files,
            plugin_location=args.plugin_location,
            model_output_dir=args.model_output_dir,
            replacement_coordinate_files=year_replacement_coordinate_files,
            run_bounds_start=run_bounds_start,
            run_bounds_end=run_bounds_end,
            sites_file=sites_file,
            suite_id=args.suite_id,
            halo_removal=grid_config["halo_removal"],
            variables=" ".join(annual_variables),
        )

        run_standalone_mip_convert(
            args.cfg_path,
            args.datestamp,
            native_convention,
        )

        for file_path in retrieved_files:
            logger.info("Removing staged monthly file %s", file_path)
            os.remove(file_path)


if __name__ == "__main__":
    main()
