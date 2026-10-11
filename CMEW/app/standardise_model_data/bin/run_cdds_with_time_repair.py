#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Run CDDS conversion with the NEMO time metadata repair injected between
extraction and MIP conversion.
"""
import argparse
import os
import shlex
import subprocess
import sys
import logging
import re
from pathlib import Path

from patch_cdds_time_repair import (
    derive_input_dir,
    derive_workflow_dir,
    patch_run_extract_app,
    read_request,
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)


def sanitise_workflow_id(workflow_id):
    """
    Return a Cylc workflow ID suitable for use in a CDDS basename.

    Cylc workflow IDs contain path separators, for example ``CMEW/run13``.
    Replace non-alphanumeric separators with underscores so the identifier
    can safely form part of a CDDS workflow and request name.
    """
    sanitised = re.sub(r"[^A-Za-z0-9._-]+", "_", workflow_id).strip("_")
    if not sanitised:
        raise ValueError(
            "CYLC_WORKFLOW_ID does not contain a usable identifier"
        )

    return sanitised


def create_parent_scoped_request(request_path, workflow_id):
    """
    Create a request copy with a parent-workflow-specific basename.

    CDDS globally registers nested Cylc workflows using
    ``cdds_<workflow_basename>``.  CMEW parent runs must therefore use
    distinct basenames so one run cannot clean another run's active CDDS
    workflow.  Keep the original generated request unchanged and write a
    sibling request used only by the standardisation task.
    """
    config = read_request(request_path)
    original_basename = config["common"]["workflow_basename"]
    workflow_suffix = sanitise_workflow_id(workflow_id)
    unique_basename = "{}_{}".format(original_basename, workflow_suffix)

    request = Path(request_path)
    unique_request_path = request.with_name(
        "{}_{}{}".format(request.stem, workflow_suffix, request.suffix)
    )

    config["common"]["workflow_basename"] = unique_basename
    with unique_request_path.open("w") as file_handle:
        config.write(file_handle)

    logger.info(
        "Created parent-scoped CDDS request %s with workflow_basename=%s",
        unique_request_path,
        unique_basename,
    )

    return str(unique_request_path)


def run_cdds_convert_no_submit(request_path):
    """
    Template and clean the nested CDDS conversion workflow without
    submitting it.

    Parameters
    ----------
    request_path : str
        The full path to the CDDS request configuration file.
    """
    logger.info("Running cdds_convert %s --no-submit", request_path)
    subprocess.run(["cdds_convert", request_path, "--no-submit"], check=True)


def submit_patched_workflow(workflow_dir, workflow_name, config):
    """
    Submit the patched conversion workflow using CDDS-equivalent
    ``cylc vip`` arguments.

    Parameters
    ----------
    workflow_dir : str
        The full path to the generated conversion workflow directory.
    workflow_name : str
        The Cylc workflow name to submit as.
    config : :class:`configparser.ConfigParser`
        The parsed CDDS request configuration.
    """
    cylc_args = shlex.split(config["conversion"]["cylc_args"])

    command = [
        "cylc",
        "vip",
        workflow_dir,
        "--no-run-name",
        "--workflow-name",
        workflow_name,
    ]

    if config.has_option("common", "simulation") and config.getboolean(
        "common", "simulation"
    ):
        command.append("--mode=simulation")

    command += cylc_args

    logger.info("Submitting patched workflow: %s", " ".join(command))
    subprocess.run(command, check=True)


def parse_args(arguments):
    """
    Return the names and values of the command line arguments for
    the orchestration script.

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
            "Run CDDS conversion with the NEMO time metadata repair "
            "injected between extraction and MIP conversion."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--request-path",
        required=True,
        help="The full path to the CDDS request configuration file.",
    )
    parser.add_argument(
        "--repair-script",
        required=True,
        help="The full path to the installed repair_nemo_time_metadata.py.",
    )
    return parser.parse_args(arguments)


def main(arguments=None):
    """
    Run CDDS conversion for a request, repairing NEMO time metadata
    between extraction and MIP conversion.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    args = parse_args(arguments)

    try:
        workflow_id = os.environ["CYLC_WORKFLOW_ID"]
    except KeyError as error:
        raise RuntimeError(
            "CYLC_WORKFLOW_ID is required to create a parent-scoped "
            "CDDS workflow name"
        ) from error

    # Use a copied request whose workflow basename includes the parent Cylc
    # workflow ID.  This prevents concurrent CMEW runs from cleaning each
    # other's globally registered nested CDDS workflows.
    scoped_request_path = create_parent_scoped_request(
        args.request_path, workflow_id
    )
    config = read_request(scoped_request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)
    workflow_name = "cdds_{}".format(config["common"]["workflow_basename"])

    # CDDS 4.0.0 provides no hook between extraction and MIP conversion.
    # Generate its parent-scoped workflow without submitting it, inject the
    # NEMO time repair after extraction, then submit it with CDDS-equivalent
    # Cylc arguments.
    run_cdds_convert_no_submit(scoped_request_path)
    patch_run_extract_app(workflow_dir, args.repair_script, input_dir)
    submit_patched_workflow(workflow_dir, workflow_name, config)


if __name__ == "__main__":
    main()
